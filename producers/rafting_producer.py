import json
import time
import random
from datetime import datetime
from confluent_kafka import Producer
from utils_generate_weather_data import generate_weather_data
from utils_generate_river_flow import generate_river_flow_data
from utils_generate_rafting_data import generate_rafting_feedback
import logging

# Kafka Configuration
KAFKA_BROKER = "localhost:9092"  # Update with actual broker address
RAFTING_TOPIC = "rafting_feedback"

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create Kafka producer
producer = Producer({"bootstrap.servers": KAFKA_BROKER})

def delivery_report(err, msg):
    """Callback for Kafka message delivery"""
    if err is not None:
        logging.error(f"Message delivery failed: {err}")
    else:
        logging.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def load_data():
    """Load data from utilities."""
    weather_data_path = generate_weather_data()
    river_data_path = generate_river_flow_data()
    feedback_data_path = generate_rafting_feedback()

    with open(weather_data_path, "r") as w_file:
        weather_data = json.load(w_file)
    with open(river_data_path, "r") as r_file:
        river_data = json.load(r_file)
    with open(feedback_data_path, "r") as f_file:
        feedback_data = json.load(f_file)
    
    return weather_data, river_data, feedback_data

def stream_data():
    """Continuously stream rafting data to Kafka."""
    weather_data, river_data, feedback_data = load_data()
    max_records = min(len(weather_data), len(river_data), len(feedback_data))
    
    for i in range(max_records):
        message = {
            "date": weather_data[i]["date"],
            "weather": weather_data[i],
            "river": river_data[i],
            "customer_feedback": feedback_data[i]
        }
        
        message_json = json.dumps(message)
        producer.produce(RAFTING_TOPIC, message_json.encode("utf-8"), callback=delivery_report)
        producer.flush()
        
        logging.info(f"Published message {i+1}/{max_records}")
        time.sleep(random.uniform(1, 3))  # Simulating real-time streaming

if __name__ == "__main__":
    logging.info("Starting Rafting Producer...")
    stream_data()
