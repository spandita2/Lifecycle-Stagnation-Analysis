# 🔄 User Lifecycle Stagnation & Churn Pipeline

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red.svg)

## 🎯 Executive Summary
Customer Acquisition Cost (CAC) leakage due to preventable churn is one of the most expensive problems in consumer tech. This project solves that by establishing a fully automated **ELT (Extract, Load, Transform)** pipeline. 

By calculating **Value-Exchange Latency** (the time elapsed since a user last derived value from the platform) and mapping it against idle capital, this system segments users into targeted risk categories. This allows marketing teams to automate targeted re-engagement campaigns for high-risk, high-value users *before* they leave.

---

## 🏗️ Technical Architecture
This project utilizes a decoupled, production-grade architecture, separating the extraction logic, computational transformations, and front-end presentation.

* ⚙️ **Data Orchestration:** A master Python script (`run_pipeline.py`) automates the sequential execution of the ELT process using the `subprocess` module.
* 🛡️ **Extraction & Quality Gates:** Simulates raw transactional ledgers and passes them through programmatic **Data Quality Gates** (null-value and anomaly detection) before database insertion to ensure analytical integrity.
* 🧠 **Database Engine:** Secure integration with a local **MySQL** database via `SQLAlchemy`, utilizing environment variables (`.env`) to protect credentials.
* 🔄 **Transformation Logic:** Shifts the heavy computational lifting to the database using advanced SQL, including **Window Functions** (`RANK() OVER`), to dynamically rank financial churn risk.
* 📊 **Full-Stack Presentation:** A live, interactive web dashboard built with **Streamlit** and **Plotly**, allowing stakeholders to filter high-risk rosters and visualize capital-at-risk in real-time.

---

## 📂 Repository Structure

```text
├── .env                        # Database credentials (Git-ignored)
├── requirements.txt            # Python dependencies
├── run_pipeline.py             # Master orchestrator script
├── 01_extract.py               # Raw data generator
├── 02_load_to_mysql.py         # Data validation and database load
├── 03_run_analysis.py          # SQL-driven transformation and segmentation
├── app.py                      # Streamlit interactive UI
└── dashboard_preview.png       # Front-end UI screenshot

🚀 Quick Start Guide
1. Clone & Install

Bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd <YOUR_FOLDER_NAME>
pip install -r requirements.txt
2. Database Configuration
Open your MySQL client and create the target database:

SQL
CREATE DATABASE IF NOT EXISTS pocket_analytics;
Create a .env file in the root directory and add your credentials:

Plaintext
MYSQL_USER=root
MYSQL_PASSWORD=your_password_here
3. Run the Automated Pipeline
Execute the master orchestrator to run extraction, validation, loading, and SQL transformation in a single command:

Bash
python run_pipeline.py
4. Launch the Dashboard
Spin up the interactive front-end:

Bash
python -m streamlit run app.py
📺 Dashboard Preview & Demo
[Insert link to your 1-minute video demo here]
