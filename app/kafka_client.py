from kafka import KafkaProducer
import json
from threading import Lock

# Module-level variables for singleton pattern
_producer = None
_lock = Lock()

def get_kafka_producer():
    global _producer
    if _producer is None:
        with _lock:  # Ensure thread safety
            if _producer is None:  # Double-checked locking
                _producer = KafkaProducer(
                    bootstrap_servers="localhost:9092",
                    value_serializer=lambda v: json.dumps(v).encode("utf-8")
                )
    return _producer