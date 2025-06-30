import json
from kafka import KafkaConsumer
# Counter used to easily count occurrences and handle missing keys
from collections import Counter


def main():
    # Create a consumer for the 'moderation-events' topic
    consumer = KafkaConsumer(
        "moderation-events",
        bootstrap_servers="localhost:9092",
        group_id="moderation-analytics-group",
        auto_offset_reset="earliest",  # Start from earliest messages if no committed offset
        enable_auto_commit=True,
        value_deserializer=lambda m: json.loads(m.decode("utf-8"))  # Automatically decode JSON
    )

    print("Listening for moderation events...")
    decision_counter = Counter()
    event_count = 0
    business_counter = Counter()
    user_counter = Counter()
    for message in consumer:
        try:
            # message.value is already a Python dict due to value_deserializer
            event = message.value
            print("New moderation event received:")
            print(json.dumps(event, indent=2, ensure_ascii=False))
            # Count moderation results
            result = event.get("moderation_result", "unknown")
            decision_counter[result] += 1

            # Count per business
            business_id = event.get("business_id", "unknown")
            business_counter[business_id] += 1

            # Count per user
            user_id = event.get("user_id", "unknown")
            user_counter[user_id] += 1

            event_count += 1

            # Load or create cumulative stats file
            try:
                with open("stats_cumul.json", "r") as f:
                    stats_cumul = json.load(f)
                    cumul_decision_counter = Counter(stats_cumul.get("decision_counts", {}))
                    cumul_business_counter = Counter(stats_cumul.get("business_counts", {}))
                    cumul_user_counter = Counter(stats_cumul.get("user_counts", {}))
                    cumul_event_count = stats_cumul.get("event_count", 0)
            except FileNotFoundError:
                cumul_decision_counter = Counter()
                cumul_business_counter = Counter()
                cumul_user_counter = Counter()
                cumul_event_count = 0

            # Update cumulative counters with current event
            cumul_decision_counter[result] += 1
            cumul_business_counter[business_id] += 1
            cumul_user_counter[user_id] += 1
            cumul_event_count += 1

            # Save updated cumulative stats
            stats_cumul = {
                "decision_counts": dict(cumul_decision_counter),
                "business_counts": dict(cumul_business_counter),
                "user_counts": dict(cumul_user_counter),
                "event_count": cumul_event_count
            }
            with open("stats_cumul.json", "w") as f:
                json.dump(stats_cumul, f)
            # Print running stats every 10 events
            if event_count % 10 == 0:
                print("\n=== Moderation Decision Counts ===")
                for decision, count in decision_counter.items():
                    print(f"{decision}: {count}")
                print("=== Counts per Business ===")
                for business, count in business_counter.items():
                    print(f"{business}: {count}")
                print("=== Counts per User ===")
                for user, count in user_counter.items():
                    print(f"{user}: {count}")
                print("==================================\n")
                # Write rolling/session stats to JSON
                stats = {
                    "decision_counts": dict(decision_counter),
                    "business_counts": dict(business_counter),
                    "user_counts": dict(user_counter),
                    "event_count": event_count
                }
                with open("stats.json", "w") as f:
                    json.dump(stats, f)
        except Exception as e:
            print(f"Error processing message: {e}")
            continue

if __name__ == "__main__":
    main()