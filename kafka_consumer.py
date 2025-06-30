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
                with open("cumul_stats.json", "r") as f:
                    cumul_stats = json.load(f)
                    cumul_decision_counter = Counter(cumul_stats.get("decision_counts", {}))
                    cumul_business_counter = Counter(cumul_stats.get("business_counts", {}))
                    cumul_user_counter = Counter(cumul_stats.get("user_counts", {}))
                    cumul_event_count = cumul_stats.get("event_count", 0)
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

            # Save updated cumulative stats for every event
            cumul_stats = {
                "decision_counts": dict(cumul_decision_counter),
                "business_counts": dict(cumul_business_counter),
                "user_counts": dict(cumul_user_counter),
                "event_count": cumul_event_count
            }
            try:
                with open("cumul_stats.json", "w") as f:
                    json.dump(cumul_stats, f)
            except Exception as file_write_error:
                print(f"Error writing cumulative stats: {file_write_error}")

            # Print running stats every 10 events
            if event_count % 10 == 0:
                print("\n=== Number of Reviews by Moderation Decision ===")
                for decision, count in decision_counter.items():
                    print(f"{decision}: {count}")
                print("=== Number of Reviews by Business ===")
                for business, count in business_counter.items():
                    print(f"{business}: {count}")
                print("=== Number of Reviews by User ===")
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