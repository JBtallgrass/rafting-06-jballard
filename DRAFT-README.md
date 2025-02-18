# **🌊 Rafting Feedback Streaming Project – Final Version**  

## **📌 Project Overview**  
Rafting adventures are thrilling, but customer feedback and environmental data are often overlooked in enhancing experiences. This project leverages **real-time analytics** to bridge that gap—tracking **customer sentiment, guide performance, and environmental conditions** to optimize rafting operations.

It integrates customer feedback with **weather** and **river conditions** to enhance **customer experience** and **guide performance** using **Apache Kafka**, **Python**, and **SQLite/PostgreSQL**.

🚀 **Key Enhancements in Final Version:**  
✅ **Optimized Kafka Consumer & Producer** with **batch processing, retries, and multi-threading**  
✅ **Enhanced SQLite Database** with **indexes & optimized schema**  
✅ **Integrated Real-Time Data Processing** for **predictive analytics**  
✅ **Built-in Visualization Support** for **Tableau & Dash (Python Web App)**  

---

## **🫠 Technologies Used**  
- **Apache Kafka** – Real-time message streaming and processing  
- **Python** – Data processing, Kafka integration, and analytics  
- **SQLite / PostgreSQL** – Database for processed data storage  
- **Matplotlib / Dash** – Data visualization and reporting  
- **Pandas** – Data manipulation and analysis  
- **Docker** *(Optional)* – For containerized Kafka and PostgreSQL  

---

## **🎯 Project Goals**  
### **1️⃣ Customer Experience Optimization**  
- Track **positive vs. negative feedback trends**  
- Identify **recurring complaints** (e.g., guide performance, safety, weather impact)  

### **2️⃣ Guide Performance Tracking**  
- Evaluate **individual guide ratings**  
- Provide **real-time alerts** for **negative reviews**  

### **3️⃣ Weather & River Conditions Analysis**  
- Assess **weather impact** on customer satisfaction  
- Predict **optimal rafting conditions** based on **historical data**  

### **4️⃣ Real-Time Alerting & Insights**  
- Detect **high-risk conditions** (e.g., dangerous river flows)  
- Provide **automated alerts** for poor guide reviews  

---

## **🔄 Workflow & Architecture**  

### **💽 Data Ingestion & Streaming**  
👉 **Data Sources:**  
- **Customer Feedback** (`utils_generate_rafting_data.py`)  
- **Weather Conditions** (`utils_generate_weather_data.py`)  
- **River Flow Levels** (`utils_generate_river_flow.py`)  

👉 **Streaming Pipeline:**  
1. `rafting_producer.py` – Reads data & streams to Kafka  
2. `rafting_consumer.py` – Reads messages, processes, and inserts into **SQLite/PostgreSQL**  

👉 **Database Processing:**  
- `db_sqlite_rafting.py` – Stores feedback, guide performance, and environmental conditions  

👉 **Real-Time Visualization:**  
- `jb_rafting_consumer.py` – Updates **live charts** for customer sentiment, guide trends, and environmental impact  

---

## **🗂 Project Components**  

### **1️⃣ Kafka Producers & Consumers**  
| Component | Description |  
|-----------|-------------|  
| `rafting_producer.py` | Streams customer feedback & environmental data to Kafka |  
| `rafting_consumer.py` | Reads Kafka messages, processes feedback, and stores in SQLite |  
| `utils_producer.py` | Handles Kafka topic creation, retries, and producer setup |  
| `utils_consumer.py` | Manages Kafka consumer with batch processing and checkpointing |  

### **2️⃣ Database & Processing**  
| Component | Description |  
|-----------|-------------|  
| `db_sqlite_rafting.py` | SQLite/PostgreSQL setup & data insertion |  
| `generate_guide_performance_report()` | Aggregates guide performance & saves as CSV |  
| `plot_guide_performance()` | Generates visualization for **guide ratings** |  

### **3️⃣ Data Generation (Synthetic Data)**  
| Component | Description |  
|-----------|-------------|  
| `utils_generate_rafting_data.py` | Creates **customer reviews** (200+ positive, 50+ negative) |  
| `utils_generate_river_flow.py` | Generates **river flow & water level data** |  
| `utils_generate_weather_data.py` | Simulates **temperature, wind, rainfall, and UV index** |  

### **4️⃣ Visualizations & Dashboard**  
| Visualization | Description |  
|--------------|-------------|  
| **Sentiment Analysis** | **Bar Chart** – Positive vs. Negative Feedback |  
| **Guide Performance** | **Stacked Bar Chart** – Guide Ratings Over Time |  
| **Weather vs. Customer Satisfaction** | **Scatter Plot** – Analyzing Impact |  
| **River Flow & Trip Satisfaction** | **Box Plot** – Correlation between flow & feedback |  

---

## **📊 Final Dashboard (Tableau/Dash)**  
This project includes a **real-time dashboard** that provides:  
✅ **Real-time trends** in customer satisfaction  
✅ **Weather & river condition alerts**  
✅ **Top-performing & underperforming guides**  
✅ **Predictive analysis on optimal rafting conditions**  

---

## **⚡ Notes & Troubleshooting**  
- **Kafka & Zookeeper must be running** before starting the producer/consumer.  
- **Common Kafka Issues:**  
  - *Broker Not Found* ➔ Check `KAFKA_BROKER_ADDRESS`
  - *Consumer Lag* ➔ Use `kafka-consumer-groups.sh --describe`
  - *High CPU/Memory Usage* ➔ Optimize batch sizes  
- **PostgreSQL Recommended** for handling large datasets.  

---

## **📚 Future Improvements**  
🔄 **Transition to PostgreSQL for large datasets**  
📊 **Develop ML-based predictive models** for customer sentiment  
🌍 **Deploy on AWS/GCP for scalability**  

💡 *Want to contribute?* Fork this repo & submit a PR!  
🔥 *Join us in revolutionizing outdoor adventure analytics!*

