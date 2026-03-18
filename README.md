# 🏙️ UrbanBot AI: Smart City Management Ecosystem

**UrbanBot AI** is an integrated, cloud-native Command Center designed to enhance urban safety and infrastructure through Deep Learning and Real-Time Analytics.

---

## 🚀 Key Modules
* **🚑 Accident Detection:** YOLOv8-powered real-time detection with automated SMTP emergency alerts.
* **🚦 Traffic & Crowd Analysis:** Dynamic monitoring of junction density to optimize urban flow.
* **🛣️ Road Damage Assessment:** Identification of potholes and structural defects to trigger maintenance logs.
* **🍃 Air Quality Predictor:** ML regression model (Pickle) providing health advisories based on pollutant data.
* **🤖 UrbanBot (RAG):** A Groq chatbot grounded strictly in AWS RDS SQL records.

---

## 🛠️ Tech Stack
* **Frontend:** Streamlit
* **Machine Learning:** Ultralytics YOLOv8, Scikit-Learn
* **LLM:** Groq llama-3.1-8b-instant (Generative AI)
* **Database:** Amazon RDS (MySQL)
* **Cloud Hosting:** Amazon EC2 (Ubuntu 24.04 LTS)
* **Language:** Python 3.10+

---

## 📦 Installation & Local Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/selvakumaran416-sketch/UrbanBot-Smart-City-Intelligence.git](https://github.com/selvakumaran416-sketch/UrbanBot-Smart-City-Intelligence.git)
   cd UrbanBot

2. **Environment Configuration:**
* Create a .env file in the root directory and add:
* DB_HOST=your-aws-rds-endpoint
* DB_PORT=your-port
* DB_USER=your-name
* DB_PASSWORD=your-password
* DB_NAME=your-DB-name
* Groq_API_KEY=your-groq-api-key
* EMAIL_USER=your-email
* EMAIL_PASS=your-app-password
* EMERGENCY_EMAIL=emergency-email

3. **Install Dependencies:**
* pip install -r requirements.txt
* python -m textblob.download_corpora

4. **Run the App:**
* streamlit run Main_App.py

## 🧩 System Modules

<img width="100" height="100" alt="image" src="https://github.com/user-attachments/assets/73479433-de4c-483d-9bb6-779098d20188" />
. **Introduction**



## ☁️ Deployment Architecture
* The system is architected for high availability on AWS. The Streamlit frontend resides on EC2, while all incident logs and system states are persisted in Amazon RDS.

## 👨‍💻 Developed By
* Selvakumaran Muthusamy Data Science Aspirant | Software Development & System Administration
