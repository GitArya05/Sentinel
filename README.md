# Sentinel: Real-Time Transaction Monitoring Engine

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Machine Learning](https://img.shields.io/badge/Machine_Learning-Scikit_Learn-orange.svg)
![Status](https://img.shields.io/badge/Status-Active_Development-brightgreen.svg)

## 📌 System Overview

Sentinel is a lightweight, real-time backend engine engineered to ingest and analyze financial data streams to detect fraudulent anomalies. Designed to process 60 heterogeneous data streams simultaneously, the system evaluates transaction metadata using probabilistic machine learning models, executing automated decision blocks within strict latency constraints (<150ms).

## 🚀 Core Architecture

- **Ingestion Layer:** Asynchronous data pipeline handling 60 simulated concurrent transaction streams.
- **Inference Engine:** Decoupled classification logic utilizing serialized Logistic Regression and Naive Bayes models.
- **Decisioning Protocol:** Automated risk mitigation executing instant protocol blocks for transaction probabilities scoring >0.8.

## 📂 Project Structure

```text
Sentinel/
├── api/             # Backend routing, configurations, and API endpoints
├── core/            # Business logic, stream simulation, and decision protocols
├── data/            # Local directory for raw/processed data (Git-ignored)
├── models/          # Serialized .pkl files for low-latency local inference
├── .gitignore
├── requirements.txt
└── README.md
```
