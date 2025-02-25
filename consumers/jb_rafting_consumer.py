import os
import json
import time
import sqlite3
from collections import defaultdict
from datetime import datetime
from kafka import KafkaConsumer
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib
matplotlib.use("TkAgg")


# Logging
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

#####################################
# Load Environment Variables
#####################################

load_dotenv()

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "172.30.179.152:9092")
KAFKA_TOPIC = os.getenv("RAFTING_TOPIC", "rafting_feedback")

if not KAFKA_BROKER or not KAFKA_TOPIC:
    logging.critical("❌ Missing required environment variables.")
    raise EnvironmentError("Missing required environment variables.")

#####################################
# Database Initialization
#####################################

DB_PATH = "rafting_feedback.db"

def initialize_database():
    """Creates the SQLite database and table if not exists."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rafting_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            guide TEXT,
            comment TEXT,
            is_negative INTEGER,
            trip_type TEXT,
            river_flow INTEGER,
            water_temperature INTEGER,
            rapid_difficulty TEXT,
            river_condition TEXT,
            timestamp TEXT
        )
    """)
    
    conn.commit()
    conn.close()
    logging.info("✅ Database initialized successfully.")

initialize_database()

#####################################
# Kafka Consumer Data Handling
#####################################

data_buffer = []
guide_feedback = defaultdict(lambda: {"positive": 0, "negative": 0})
weekly_feedback = defaultdict(lambda: {"positive": 0, "negative": 0})
negative_feedback_log = []

def insert_feedback_into_db(message):
    """Inserts feedback data into the SQLite database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO rafting_feedback 
            (date, guide, comment, is_negative, trip_type, river_flow, water_temperature, rapid_difficulty, river_condition, timestamp) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            message.get("date", "unknown"),
            message.get("guide", "unknown"),
            message.get("comment", "No comment provided"),
            int(message.get("is_negative", False)),  # Convert boolean to integer (0 = positive, 1 = negative)
            message.get("trip_type", "unknown"),
            message.get("river_flow", 0),
            message.get("water_temperature", 0),
            message.get("rapid_difficulty", "unknown"),
            message.get("river_condition", "unknown"),
            message.get("timestamp", datetime.utcnow().isoformat())
        ))

        conn.commit()
        conn.close()
        logging.info(f"📥 Data inserted into SQLite for guide: {message.get('guide')}")
    
    except Exception as e:
        logging.error(f"❌ Error inserting feedback into database: {e}")

#####################################
# Message Processing
#####################################

def process_message(message):
    """Processes incoming Kafka messages and updates tracking data."""
    try:
        guide = message.get("guide", "unknown")
        comment = message.get("comment", "No comment provided")
        is_negative = message.get("is_negative", False)
        trip_date = message.get("date", "unknown")

        week_number = datetime.strptime(trip_date, "%Y-%m-%d").isocalendar()[1]
        feedback_type = "negative" if is_negative else "positive"

        guide_feedback[guide][feedback_type] += 1
        weekly_feedback[(guide, week_number)][feedback_type] += 1

        if is_negative:
            negative_feedback_log.append(message)

        insert_feedback_into_db(message)  # Store message in SQLite
        
        logging.info(f"📝 Feedback ({trip_date}) | Guide: {guide} | Comment: {comment}")

    except Exception as e:
        logging.error(f"❌ Error processing message: {e}")

#####################################
# Real-Time Visualization
#####################################

def update_chart(frame):
    """Fetches data from SQLite and updates visualization in real-time."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM rafting_feedback", conn)
    conn.close()

    if df.empty:
        return

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["week"] = df["date"].dt.isocalendar().week

    plt.clf()
    plt.subplot(2, 2, 1)
    plot_sentiment_distribution(df)
    
    plt.subplot(2, 2, 2)
    plot_weekly_trend(df)
    
    plt.subplot(2, 2, 3)
    plot_guide_performance(df)
    
    plt.subplot(2, 2, 4)
    plot_negative_feedback_trend(df)
    
    plt.tight_layout()

#####################################
# Visualization Functions
#####################################

def plot_weekly_trend(df):
    weekly_counts = df.groupby('week')['is_negative'].value_counts().unstack().fillna(0)

    # Ensure correct column assignment based on actual data
    if weekly_counts.shape[1] == 2:
        weekly_counts.columns = ['Positive', 'Negative']
    elif weekly_counts.shape[1] == 1:
        weekly_counts.columns = ['Positive'] if 0 in weekly_counts.columns else ['Negative']

    weekly_counts.plot(kind='line', ax=plt.gca())
    plt.title("Weekly Feedback Trend")
    plt.xlabel("Week Number")
    plt.ylabel("Feedback Count")

def plot_guide_performance(df):
    guide_counts = df.groupby('guide')['is_negative'].value_counts().unstack().fillna(0)
    guide_counts.columns = ['Positive', 'Negative']
    guide_counts.plot(kind='bar', stacked=True, ax=plt.gca())
    plt.title("Guide Performance (Positive vs Negative)")
    plt.xlabel("Guide")
    plt.ylabel("Feedback Count")
    plt.xticks(rotation=45)

def plot_negative_feedback_trend(df):
    negative_feedback = df[df['is_negative'] == 1].copy()
    negative_feedback.groupby('date').size().plot(kind='line', ax=plt.gca())
    plt.title("Daily Negative Feedback Trend")
    plt.xlabel("Date")
    plt.ylabel("Count of Negative Feedback")

def plot_sentiment_distribution(df):
    feedback_counts = df['is_negative'].value_counts()
    feedback_counts.index = ['Positive', 'Negative'] if len(feedback_counts) == 2 else ['Positive']
    feedback_counts.plot(kind='pie', autopct='%1.1f%%', ax=plt.gca())
    plt.title("Sentiment Distribution")
    plt.ylabel("")

#####################################
# Main Kafka Consumer Loop
#####################################

def main():
    logging.info("🚀 Starting Kafka consumer for rafting feedback.")
    
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset="earliest",
        group_id="rafting_consumer_group",
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )

    fig = plt.figure(figsize=(12, 10))
    global ani
    ani = FuncAnimation(fig, update_chart, interval=2000)

    try:
        for message in consumer:
            message_dict = message.value
            process_message(message_dict)
            data_buffer.append(message_dict)

            if len(data_buffer) > 1000:
                data_buffer.pop(0)

            time.sleep(0.5)
    except KeyboardInterrupt:
        logging.warning("⚠️ Consumer interrupted by user.")
    except Exception as e:
        logging.error(f"❌ Error in Kafka consumer: {e}")
    finally:
        plt.show()
        consumer.close()

#####################################
# Conditional Execution
#####################################

if __name__ == "__main__":
    main()
