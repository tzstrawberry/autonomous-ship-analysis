# Autonomous Ship Data Analysis Pipeline

## 📌 Project Overview

This project implements a Python-based data analysis pipeline for the simulation and evaluation of sensor data from an autonomous inland vessel.

Since no real-world data is available, synthetic (simulated) sensor data is generated.

The goal is to compute and analyze key operational metrics such as:

- Energy consumption (Wh/km)  
- Data density (GB/h)  
- Environmental conditions (e.g., wind speed)  

---

## ⚙️ Project Structure

autonomous-ship-analysis/

├── data/
├── src/
│   ├── generate_data.py
│   ├── clean.py
│   ├── metrics.py
│   └── visualize.py
│
├── main.py
├── requirements.txt
└── README.md

---

## 📊 Data Description

The dataset is synthetic (simulated).

It includes:

- timestamp  
- speed  
- power_w  
- wind_speed  
- distance  

---

## 🚀 How to Run

Install dependencies:

pip install -r requirements.txt

Run:

python main.py

---

## 📈 Output

- Generate data  
- Process data  
- Compute metrics  
- Visualize results  

---

## 🛠️ Technologies

- Python  
- Pandas  
- NumPy  
- Matplotlib  

---

## 📌 Purpose

- Data simulation  
- Data analysis  
- Metric calculation  
- Visualization  

---

# 🇩🇪 Deutsche Version

## 📌 Projektübersicht

Dieses Projekt implementiert eine Python-basierte Analysepipeline zur Simulation von Sensordaten eines autonomen Binnenschiffs.

Es werden synthetische Daten erzeugt, da keine realen Daten vorhanden sind.

Ziel ist die Berechnung von Kennzahlen wie:

- Energieverbrauch (Wh/km)  
- Datendichte (GB/h)  
- Umweltbedingungen  

---

## 🚀 Ausführung

pip install -r requirements.txt  
python main.py
