<!-- PROJECT TITLE -->

<h1 align="center">APS Fault Detection</h1>

<h3 align="center">
AI-Powered Detection of Critical Failures Before They Happen using Sensor Data and Machine Learning
</h3>

<p align="center">

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/XGBoost-FF6F00?style=for-the-badge&logo=apache&logoColor=white"/>
<img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
<img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
<img src="https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white"/>
<img src="https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white"/>
<img src="https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white"/>
<img src="https://img.shields.io/badge/ScikitLearn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white"/>
<img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white"/>

</p>

---

## 📌 Project Overview

APS Fault Detection is an end-to-end Machine Learning system developed to identify failures in aps of vehicles using sensor data.

APS stands for **Air Pressure System**, which is a critical subsystem used in heavy vehicles such as trucks and buses. The APS is responsible for operating important components including **air brakes, suspension systems, and other pressure-based mechanisms** that ensure safe and efficient vehicle operation.

Modern heavy vehicles are equipped with numerous sensors that continuously collect data about the condition of different components. These sensors generate large volumes of data that can be analyzed to detect abnormal patterns and system failures.

This project uses machine learning techniques to analyze sensor measurements and determine whether there is a fault in the **Air Pressure System (APS)** or not.

The final goal of the project is to **detect potential APS failures early using predictive analytics**, allowing vehicle operators to take preventive actions before serious system failures occur.

---

## 🎯 Problem Statement

Heavy vehicles rely on multiple subsystems to operate safely and efficiently, and the Air Pressure System (APS) plays a crucial role in enabling key functionalities such as braking and suspension. However, inspecting APS components in heavy vehicles is often **time-consuming and expensive**. As a result, regular manual inspections are sometimes skipped or delayed in real-world operations.

When APS faults remain undetected, they can lead to **serious safety risks, unexpected breakdowns, and even road accidents**. Since failures may occur suddenly without clear warning signs, it becomes difficult for operators to determine whether the APS is functioning properly.

Therefore, there is a need for an intelligent system capable of **analyzing sensor data automatically and identifying potential APS failures before they lead to critical issues**.

---
## 💡 Proposed Solution

To address this problem, this project proposes a **machine learning-based predictive system** that analyzes sensor data collected from heavy vehicles and determines whether there's a failure in the Air Pressure System (APS) or not.

The system processes sensor readings through a structured machine learning pipeline, where the data is first cleaned, validated, and transformed before being used to train an advanced classification model.

An **XGBoost machine learning model** is used to learn patterns from historical sensor data and accurately classify system conditions.

By using this predictive model, vehicle operators can identify potential APS faults without performing expensive and unnecessary manual inspections.

The proposed solution offers several benefits:

• **Early detection of APS failures** before critical breakdowns occur  
• **Reduction in unnecessary inspection costs** by performing checks only when the model predicts a potential issue  
• **Improved vehicle safety** by preventing accidents caused by undetected system faults  
• **Efficient utilization of sensor data** for intelligent decision-making  

The trained model is deployed using **FastAPI**, containerized with **Docker**, and integrated with **AWS cloud services**, enabling scalable and real-time predictions through an API-based system.

This approach transforms traditional maintenance practices into a **data-driven predictive system**, improving reliability, safety, and operational efficiency.

---

# 🧠 Machine Learning Objective
The model predicts:
| Prediction | Meaning |
|-----------|--------|
| pos | APS Failure |
| neg | No Failure in APS |

---

# 📊 Dataset Description
The dataset contains **sensor measurements collected from heavy vehicles**.
Each record represents readings from multiple sensors installed in the vehicle system.
Dataset Characteristics:
- High dimensional sensor data
- Presence of missing values
- Imbalanced class distribution

--- 

## ⚙️ Machine Learning Pipeline
This project follows a modular Machine Learning architecture consisting of multiple pipeline components.
Each component is implemented as an independent module to maintain scalability and maintainability.
<p>
<h4 align="center">

📥 <b>Data Ingestion</b>  
⬇️  
🔍 <b>Data Validation</b>  
⬇️  
⚙️ <b>Data Transformation</b>  
⬇️  
🧠 <b>Model Training (XGBoost)</b>  
⬇️  
📊 <b>Model Evaluation</b>  
⬇️  
📦 <b>Model Pusher</b>  
⬇️  
🚀 <b>Model Deployment (FastAPI + Docker + AWS)</b>  
</h4>
</p>

---

## 📈 Model Performance

The final XGBoost model achieved the following performance:
| Training Accuracy | 99.99% |
|------|------|

| Testing Accuracy | 98.99% |
|------|------|


Cost Analysis:  
False Positive Cost : Lower maintenance cost  
False Negative Cost : High failure cost  

Final Cost Metrics:
| Cost Function | 1930 |
|------|------|

| Total Cost Prediction | 1886 |
|------|------|

---

## 🛠️ Technologies Used

| Category | Tools / Technologies |
|----------|----------------------|
| Programming Language | Python |
| Machine Learning | XGBoost, Scikit-learn |
| Data Processing | Pandas, NumPy |
| Backend API | FastAPI |
| Database | MongoDB |
| Containerization | Docker |
| Cloud Platform | AWS (EC2, ECR, S3) |
| CI/CD | GitHub Actions |

---

## ▶️ Running the Project

Clone the repository: git clone https://github.com/KeshaviVerma/APS_Fault_Detection.git  
Install dependencies: pip install -r requirements.txt  
Start FastAPI server: python main.py  
Open browser: http://localhost:8080/docs  

---

## 🔗 API Endpoints

The system exposes APIs for training and prediction.

| Endpoint | Method | Description |
|---------|--------|-------------|
| `/` | GET | Redirects to API docs |
| `/train` | GET | Triggers the complete ML training pipeline including data ingestion, validation, transformation, model training, evaluation, and deployment. |
| `/predict` | POST | Upload a CSV file containing sensor data. The API processes the data and returns predictions indicating whether APS failure is detected. |

---

# 🐳 Docker Container

The application runs inside a Docker container.  

docker build -t aps_fault_detection   
docker run -p 8080:8080 aps_fault_detection  

---

# ☁️ AWS Deployment

Deployment uses:

• AWS EC2  
• AWS ECR  
• AWS S3  
• GitHub Actions CI/CD  

The application is deployed using a containerized architecture.
<p>
<h4 align="center">
Deployment Architecture:
</h4>
<h4 align="center">

GitHub  
↓  
GitHub Actions  
↓  
Docker Image Build  
↓  
Push to AWS ECR  
↓  
Deploy on EC2  
</h4>

This ensures automated model deployment and scalable API services.  

---

## 🔮 Future Improvements

• Real-time sensor streaming  
• Dashboard for monitoring predictions  
• Advanced model monitoring  
• Integration with vehicle IoT systems

---

<p align="center">
⭐ If you found this project helpful, please star the repository.
<br>
<img src="https://img.shields.io/github/stars/KeshaviVerma/APS_Fault_Detection?style=social"/>
</p>