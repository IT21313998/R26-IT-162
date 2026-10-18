# An Intelligent IoT-Based Flood Early Warning & Water Level Prediction System for Kelani Riverine Communities in Sri Lanka

[![SLIIT CDAP](https://img.shields.io/badge/SLIIT-CDAP%202026-0056b3.svg)](http://cdap.sliit.lk/)
[![Project ID](https://img.shields.io/badge/Project%20ID-R26--IT--162-blue.svg)](#)
[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
[![Hardware](https://img.shields.io/badge/Hardware-ESP32%20%7C%20SIM800L-brightgreen)](https://www.espressif.com/)
[![Broker](https://img.shields.io/badge/MQTT-EMQX%20Broker-orange)](https://www.emqx.io/)
[![License](https://img.shields.io/badge/License-Academic%20Research-lightgrey.svg)](#)

---

## 📌 Executive Summary

Flooding is a recurrent and catastrophic hazard along Sri Lanka's **Kelani River basin**. The disaster triggered by Cyclone Ditwah in November 2025 affected over **2.2 million citizens**, displaced 165,000 residents, and caused 646 fatalities. Conventional early-warning mechanisms rely on manual river gauge monitoring and generalized public bulletins, creating critical spatial and temporal warning gaps.

This project (**R26-IT-162**) presents an end-to-end cyber-physical architecture combining:
1. **Hyperlocal IoT Telemetry**: Solar-powered ESP32 sensor nodes equipped with tipping bucket and ultrasonic rain-cup gauges transmitting real-time rainfall over GPRS (`broker.emqx.io`).
2. **Atmospheric Data Fusion**: Dynamic ingestion of surface pressure, dew point depression ($T - T_{dew}$), and wind vectors from Open-Meteo.
3. **Multi-Horizon ML Forecasting**: Multi-stage gradient boosting (LightGBM/XGBoost) and Bi-LSTM models delivering continuous **24-hour, 48-hour, and 72-hour rainfall predictions** ($R^2 > 0.88$).
4. **Distance-Based Dynamic Flood Risk Scoring (DFRS)**: Downstream partner model forecasting river water levels and generating trilingual early warnings (Sinhala, Tamil, English).

---

## 👥 Research Team & Supervision

| Role | Member Name | Student ID | Specialization / Component |
| :--- | :--- | :--- | :--- |
| **Lead Researcher (Student A)** | **Rasara S.H.K** | `IT21313998` | Hyperlocal IoT Rain Gauging & Multi-Horizon ML Forecasting |
| **Researcher (Student B)** | **U.H.K Sankalana** | `IT22236814` | Water Level Hydrological Modeling & Dynamic Flood Risk Scoring (DFRS) |
| **Research Supervisor** | **Ms. Tharushi Rubasinghe** | - | Department of Information Technology, SLIIT |
| **Research Co-Supervisor** | **Ms. Sameeri Subasinghe** | - | Department of Information Technology, SLIIT |

- **Institution**: Sri Lanka Institute of Information Technology (SLIIT)
- **Faculty / Dept**: Faculty of Computing, Department of Information Technology
- **Research Cluster**: Technology Integration and Management (TIM) / Center of Excellence in AI (CoEAI)
- **Batch**: 2026 Regular Batch

---

## 🏛️ System Architecture

```
  +-------------------------------------------------------------+
  |              FIELD IOT RAINFALL SENSING LAYER               |
  |  - ESP32 Microcontroller + FreeRTOS                         |
  |  - Ultrasonic Rain Cup Gauge (0-125 ml)                     |
  |  - Auto-Draining Solenoid Valve Relay (GPIO 25)             |
  |  - SIM800L GSM/GPRS Modem (APN: dialogbb)                   |
  +------------------------------+------------------------------+
                                 |
                                 | MQTT (broker.emqx.io:1883)
                                 v
  +-------------------------------------------------------------+
  |                REAL-TIME DATA FUSION HUB                    |
  |  - src/mqtt_subscriber.py : Listens to smart_irrigation/#   |
  |  - src/live_weather_api.py : Live Open-Meteo API Ingestion  |
  |    (Pressure Tendency, RH, Magnus Dew Point, Wind Vector)   |
  +------------------------------+------------------------------+
                                 |
                                 v
  +-------------------------------------------------------------+
  |           MULTI-HORIZON ML INFERENCE ENGINE                 |
  |  - src/fusion_engine.py & src/iot_predictor.py              |
  |  - Multi-Horizon Models: Day +1 (24h), Day +2 (48h), Day +3 |
  |  - Gradient Boosters (LightGBM, XGBoost) & Bi-LSTM          |
  +------------------------------+------------------------------+
                                 |
                +----------------+----------------+
                |                                 |
                v                                 v
  +---------------------------+     +---------------------------+
  |  STUDENT B REST API       |     |  STREAMLIT DASHBOARD      |
  |  GET /api/v1/forecast     |     |  - Live Hardware Stream   |
  |  - 24h/48h/72h Rainfall   |     |  - Kelani Gauging Map     |
  |  - Flood Risk Tier        |     |  - Storm Sandbox Sim      |
  +---------------------------+     +---------------------------+
```

---

## 📂 Repository Directory Structure

```text
R26-IT-162/
├── .gitignore                      # Git exclusion rules
├── README.md                       # Master research documentation
├── requirements.txt                # Python environment dependencies
│
├── arduino_esp32/                  # Component A: Embedded Firmware
│   └── esp32_rain_hivemq.ino       # ESP32 + SIM800L + Ultrasonic + Valve source
│
├── cdap_website/                   # Academic Information Website (SLIIT Course Web)
│   ├── index.html                  # Home & Executive Abstract
│   ├── domain.html                 # Literature Review, Objectives & Methodology
│   ├── milestones.html             # Assessment Schedule & Marks Breakdown
│   ├── documents.html              # Academic Document Repository
│   ├── presentations.html          # Proposal & Progress Slide Decks
│   ├── about.html                  # Research Team & Supervisor Profiles
│   ├── contact.html                # Official Inquiries Form
│   ├── css/style.css               # Modern responsive styling
│   ├── js/main.js                  # Navigation & interactive logic
│   └── docs/                       # Embedded PDFs (Charter, Proposal, Logbook)
│
├── dashboard/                      # Interactive Evaluation Dashboard
│   └── app.py                      # Multi-tab Streamlit viva presentation UI
│
├── data/                           # Hydrological & Meteorological Datasets
│   ├── raw/                        # 3.65 Years (31,992 hrs) Kelani climate data
│   └── processed/                  # Feature engineered time-series matrices
│
├── docs/                           # Official Academic Submissions (PDFs)
│   ├── Project_Charter_R26_IT_162.pdf
│   ├── Proposal_Report_IT21313998.pdf
│   ├── BiWeekly_Logbook_IT21313998.pdf
│   ├── Declaration_IT21313998.pdf
│   └── Declaration_IT22236814.pdf
│
├── models/                         # Serialized Machine Learning Artifacts
│   └── rain_model_bundle.joblib    # Trained multi-horizon LightGBM/XGBoost models
│
├── notebooks/                      # Exploratory Data Analysis & Model Training
│   └── rain_prediction_colab.ipynb # 31-cell Google Colab benchmark notebook
│
└── src/                            # Core Application Source Code
    ├── api_server.py               # FastAPI partner endpoint for Student B
    ├── fusion_engine.py            # Real-time IoT + API atmospheric data fusion
    ├── iot_predictor.py            # Multi-horizon inference & thermodynamic fallback
    ├── live_weather_api.py         # Open-Meteo live climate ingestion
    └── mqtt_subscriber.py          # EMQX MQTT background subscriber
```

---

## 🚀 Quick Start Guide

### 1. Environment Setup

Clone repository and install dependencies:
```bash
git clone https://github.com/IT21313998/R26-IT-162.git
cd R26-IT-162

# Create virtual environment
python -m venv venv
venv\Scripts\activate      # Windows

# Install required packages
pip install -r requirements.txt
```

### 2. Launching the Interactive Streamlit Dashboard

```bash
cd dashboard
python -m streamlit run app.py
```
Open `http://localhost:8501` to access:
- **Live Hardware Telemetry**: Live water volume, distance, fill rate, and valve state.
- **Multi-Horizon Predictions**: 24h, 48h, and 72h forecasted rainfall (mm) and flood alert tier.
- **Storm Sandbox Simulation**: Real-time simulation of Monsoonal, Normal, and Cyclone Ditwah events.
- **Kelani River Basin Map**: Spatial GIS representation of gauging stations.

### 3. Launching Student B Partner REST API

```bash
uvicorn src.api_server:app --host 0.0.0.0 --port 8000 --reload
```
- Interactive Swagger Documentation: `http://localhost:8000/docs`
- Latest Forecast Endpoint: `GET http://localhost:8000/api/v1/forecast/latest`

---

## 📊 Model Performance Benchmarks

Trained on 31,992 hourly climate observations (2021–2025) across Kelani Basin stations:

| Horizon | Baseline (Ridge/LogReg) | Random Forest | XGBoost | LightGBM (Selected) | Bi-LSTM |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Day +1 (24h) MAE** | 8.42 mm | 4.85 mm | 3.92 mm | **3.61 mm** | 3.75 mm |
| **Day +2 (48h) MAE** | 12.15 mm | 6.42 mm | 5.30 mm | **4.98 mm** | 5.12 mm |
| **Day +3 (72h) MAE** | 16.80 mm | 8.90 mm | 7.45 mm | **6.82 mm** | 7.05 mm |
| **Rain Detection F1** | 0.68 | 0.81 | 0.86 | **0.88** | 0.87 |

---

## 🌿 Sustainable Development Goals (SDGs)

This research contributes to the United Nations Sustainable Development Goals:
- **SDG 11**: *Sustainable Cities and Communities* — Target 11.5 (Disaster Risk Reduction).
- **SDG 13**: *Climate Action* — Target 13.1 (Strengthening resilience to climate-related hazards).
- **SDG 1**: *No Poverty* — Protecting livelihoods and vulnerable riverine settlements from flood damage.

---

## 📄 License & Attribution

Developed as an undergraduate research project for the **B.Sc. (Hons) in Information Technology** degree at the **Sri Lanka Institute of Information Technology (SLIIT)**.

&copy; 2026 Research Group R26-IT-162. All rights reserved.
