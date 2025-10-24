"""
agents/agent-interactive/kafka_produce_event.py
---------------------------------
Simple test producer for Kafka.  Sends one mock network event
to topic defined in .env (KAFKA_TOPIC_IN).
"""

import os, json, time
from dotenv import load_dotenv
from kafka import KafkaProducer

load_dotenv()

BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
TOPIC = os.getenv("KAFKA_TOPIC_IN", "network.events.raw")

# sample event payload
event = {
    "device_name": "A-RR-1",
    "ip": "192.168.100.111",
    "symptom": "Interface Gi0/0/0/1 down, CRC errors",
    "severity": "major",
    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
}

print(f"[INFO] Sending event to topic '{TOPIC}' on broker '{BROKER}'...")
producer = KafkaProducer(
    bootstrap_servers=[BROKER],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)
producer.send(TOPIC, event)
producer.flush()
print("[INFO] Event published successfully.")