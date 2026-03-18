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

# 1. **Introduction**
<img width="1920" height="1375" alt="Introduction" src="https://github.com/user-attachments/assets/b72188fa-57cd-4b05-b661-81f7a9e0f392" />

# 2. **Dashboard**
<img width="1920" height="1447" alt="Dashboard" src="https://github.com/user-attachments/assets/4e830363-652f-473b-9e19-080bb41cc713" />

# 3. **Accident Detection**
<img width="1920" height="1145" alt="Accident" src="https://github.com/user-attachments/assets/c5ba10d3-b52e-4587-93f1-973b4a074c1f" />

# 4. **Traffic Detection**
<img width="1920" height="1317" alt="Traffic" src="https://github.com/user-attachments/assets/0aec80cc-e82c-422e-9c2a-00d1691e611e" />

# 5. **Crowd Detection**
<img width="1920" height="1192" alt="Crowd" src="https://github.com/user-attachments/assets/7d8f2509-b07a-4a7b-b096-1f1a42af371e" />

# 6. **Road Damage Detection**
<img width="1920" height="1431" alt="Road_Damage" src="https://github.com/user-attachments/assets/4fdcfae1-95fb-4156-bb42-73ad6209947f" />

# 7. **Air Quality Detection**
<img width="1920" height="1445" alt="Air_Quality" src="https://github.com/user-attachments/assets/c0c06bf1-3421-431f-b6c5-746978343d3b" />

# 8. **Citizen Complaints**
<img width="1920" height="1900" alt="Citizen_Complaints" src="https://github.com/user-attachments/assets/6385ce8b-7eca-455f-a60e-cd0b536063c1" />

# 9. **Chat Bot**
<img width="1920" height="2325" alt="Chat_bot" src="https://github.com/user-attachments/assets/c742c1b8-52f5-45b3-81f6-a4a428bab181" />

# 10. **Developer Profile**
<img width="1920" height="2055" alt="Profile" src="https://github.com/user-attachments/assets/65343d7a-1368-4ba6-94ce-7a844546fa79" />

## ☁️ Deployment Architecture
* The system is architected for high availability on AWS. The Streamlit frontend resides on EC2, while all incident logs and system states are persisted in Amazon RDS.

## 👨‍💻 Developed By
* Selvakumaran Muthusamy Data Science Aspirant | Software Development & System Administration
