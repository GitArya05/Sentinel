# Sentinel: Real-Time Transaction Monitoring Engine

![Python](https://img.shields.io/badge/Python-3.10+-007EC6?style=flat-square&logo=python&logoColor=white)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Scikit%20Learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active%20Development-4C1?style=flat-square)

Sentinel is a real-time, cloud-native microservice architecture designed to detect anomalous transaction patterns and intercept fraudulent activity. It utilizes a split-architecture model, decoupling a high-fidelity data visualization frontend from a stateless, asynchronous machine learning inference API.

## 🚀 Live Deployment
**Access the live dashboard here:** [Sentinel Analytics Dashboard](https://sentinel-t9sl5mamcyjjetzac9smbz.streamlit.app/)

*Note: The backend inference engine is hosted on a free-tier Render instance. If the service has been inactive, the initial cold-start inference may take ~50 seconds to resolve. Subsequent requests execute in <100ms.*

## 🏗 System Architecture
Sentinel operates on a decoupled client-server model to ensure horizontal scalability:

1. **Inference Engine (Backend):** A stateless `FastAPI` microservice hosted on Render. It exposes RESTful endpoints (`/api/v1/transaction`) that deserialize incoming JSON payloads, route them through a pre-trained `scikit-learn` predictive model loaded into RAM, and return asynchronous risk assessments.
2. **Analytics Dashboard (Frontend):** A `Streamlit` application hosted on Streamlit Community Cloud. It manages the user state, securely passes environmental secrets, and renders interactive `Plotly` data visualizations based on the API's JSON responses.

## ⚙️ Core Capabilities
- **Sub-100ms Inference:** Asynchronous API endpoints ensure non-blocking prediction serving.
- **Defensive Error Handling:** Built-in graceful degradation; if the ML model artifact is unavailable, the API defaults to a safe state without crashing the server.
- **Dynamic Risk Scoring:** Calculates distinct probability floats for every transaction, translating raw model outputs into actionable `APPROVED` or `BLOCKED` directives.
- **Environment Isolation:** Secrets and backend routing URLs are abstracted from the codebase using cloud-native environment variables.

## 💻 Tech Stack
- **Machine Learning:** `scikit-learn`, `pandas`, `joblib`
- **Backend API:** `FastAPI`, `Uvicorn`, `Pydantic` (Data Validation)
- **Frontend UI:** `Streamlit`, `Plotly`, `Pydeck`, `Requests`
- **DevOps:** `Git`, `Render` (PaaS), `Streamlit Cloud`

## 📸 Interface Preview
<img width="1911" height="470" alt="Screenshot 2026-05-25 152945" src="https://github.com/user-attachments/assets/4cc1789a-4c18-4662-ad7c-e251abbcc1e8" />

<img width="1919" height="754" alt="Screenshot 2026-05-25 153015" src="https://github.com/user-attachments/assets/baae6c5d-b387-49be-b9dc-8e260f4ac376" />

<img width="1918" height="746" alt="Screenshot 2026-05-25 153152" src="https://github.com/user-attachments/assets/bbda61a2-c576-4d6a-b105-6cb6577871f3" />

<img width="1794" height="687" alt="Screenshot 2026-05-25 153220" src="https://github.com/user-attachments/assets/3a7a3b99-bc28-44ed-b595-fd4c27239ff1" />

<img width="1788" height="716" alt="Screenshot 2026-05-25 153413" src="https://github.com/user-attachments/assets/71bcd2e8-8ddd-45f7-9476-c9f61cfe28ca" />

## 🛠 Local Development

**1. Clone the repository**
```bash
git clone [https://github.com/GitArya05/Sentinel.git](https://github.com/GitArya05/Sentinel.git)
cd Sentinel
