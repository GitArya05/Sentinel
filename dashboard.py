# dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.graph_objects as go
import time
import random
from datetime import datetime
import os

# Dynamic Environment Routing
# Defaults to localhost for local testing, but uses the cloud URL if deployed
API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000/api/v1/transaction")

# --- UI Configuration ---
st.set_page_config(
    page_title="Sentinel: Fraud Analytics Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🛡️ Sentinel: Fraud Analytics Dashboard")
st.markdown("Real-time monitoring of heterogeneous transaction patterns")

# --- Location Mapping for Geo-Spatial Anomaly Map ---
GEO_MAP = {
    "Mumbai": [72.8777, 19.0760], "Delhi": [77.1025, 28.7041],
    "Bangalore": [77.5946, 12.9716], "Hyderabad": [78.4867, 17.3850],
    "Pune": [73.8567, 18.5204], "Nagpur": [79.0882, 21.1458]
}

# --- State Management ---
if 'total_txns' not in st.session_state:
    st.session_state.total_txns = 11547
if 'fraud_cases' not in st.session_state:
    st.session_state.fraud_cases = 319

# --- Top Level Metrics (with Delta tracking) ---
col1, col2, col3, col4 = st.columns(4)

new_txns = random.randint(10, 50)
st.session_state.total_txns += new_txns
new_fraud = 1 if random.random() < 0.05 else 0
st.session_state.fraud_cases += new_fraud
current_latency = max(80, min(150, int(np.random.normal(120, 15))))

with col1:
    st.metric("Total Transactions", f"{st.session_state.total_txns:,}", f"+{new_txns} /sec")
with col2:
    st.metric("Fraud Cases Detected", f"{st.session_state.fraud_cases}", f"+{new_fraud} recent", delta_color="inverse")
with col3:
    st.metric("System Accuracy", "98.2%", "Optimized")
with col4:
    st.metric("Avg. Latency", f"{current_latency}ms", "-5ms", delta_color="normal")

st.markdown("---")

# --- High-End Plotly Transaction Stream ---
st.subheader("Transaction Volume Over Time")
colors = ['#00d2ff', '#3a7bd5', '#ff512f', '#dd2476', '#11998e']
fig = go.Figure()

for i in range(5):
    y_data = np.random.randn(20) * 2000 + 5000
    fig.add_trace(go.Scatter(
        y=y_data, 
        mode='lines', 
        name=f'Stream_0{i+1}',
        line=dict(width=2, color=colors[i]),
        fill='tozeroy', # Adds a beautiful glowing gradient below the lines
        fillcolor=f"rgba{tuple(list(int(colors[i].lstrip('#')[j:j+2], 16) for j in (0, 2, 4)) + [0.1])}"
    ))

fig.update_layout(
    template="plotly_dark",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=0, r=0, t=10, b=0),
    height=350,
    xaxis=dict(showgrid=False, visible=False),
    yaxis=dict(showgrid=True, gridcolor='#333333')
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# --- Fixed Geographic Anomaly Detection ---
st.subheader("Geographic Anomaly Detection")
st.markdown("*Hover over anomalies to view intensity. Scroll from the page edges to bypass map zoom.*")

map_data = []
for _ in range(50):
    if random.random() < 0.3:
        loc = random.choice(list(GEO_MAP.values()))
        map_data.append({"lon": loc[0] + random.uniform(-0.1, 0.1), "lat": loc[1] + random.uniform(-0.1, 0.1), "color": [255, 75, 75, 200], "radius": 15000})
    else:
        map_data.append({"lon": random.uniform(-130, 130), "lat": random.uniform(-50, 60), "color": [255, 0, 0, 255], "radius": 40000})

df_map = pd.DataFrame(map_data)

# Switching to 'carto' fixes the black void map. Pitch=45 gives a 3D enterprise look.
st.pydeck_chart(pdk.Deck(
    map_provider="carto",
    map_style="dark",
    initial_view_state=pdk.ViewState(
        latitude=20.0,
        longitude=0.0,
        zoom=1.2,
        pitch=45, 
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=df_map,
            get_position='[lon, lat]',
            get_color='color',
            get_radius='radius',
            pickable=True,
            auto_highlight=True
        ),
    ],
    tooltip={"text": "Anomaly Detected\nRisk Score: 0.99"}
))

st.markdown("---")

# --- Recent Fraud Alerts (Cleaned Table) ---
st.subheader("Recent Fraud Alerts")

alerts = []
for _ in range(8):
    alerts.append({
        "Transaction ID": f"{random.choice('abcdef0123456789')}{random.randint(1000,9999)}...{random.randint(1000,9999)}",
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Sender": f"user{random.randint(10,99)}@okaxis",
        "Amount (INR)": f"₹ {round(random.uniform(20000, 80000), 2):,}",
        "Location": "Foreign_IP" if random.random() > 0.5 else random.choice(list(GEO_MAP.keys())),
        "Risk Score": round(random.uniform(0.85, 1.0), 2),
        "Action": "🚨 BLOCKED"
    })

df_alerts = pd.DataFrame(alerts)

# hide_index removes the ugly number column on the left
st.dataframe(
    df_alerts, 
    use_container_width=True, 
    hide_index=True,
    column_config={
        "Risk Score": st.column_config.ProgressColumn(
            "Risk Score", format="%.2f", min_value=0, max_value=1
        )
    }
)

time.sleep(3)

import requests # Make sure this is imported at the top of your file!

st.markdown("---")
# --- Manual Ad-Hoc Investigation ---
st.subheader("🕵️ Manual Transaction Scanner")
st.markdown("Input raw transaction data to ping the real-time inference API.")

with st.form("manual_scan_form"):
    col1, col2 = st.columns(2)
    with col1:
        txn_amount = st.number_input("Amount (INR)", min_value=1.0, value=50000.0)
        txn_category = st.selectbox("Merchant Category", ["Retail", "Food & Beverage", "Travel", "Utility", "Transfer", "Crypto"])
    with col2:
        txn_location = st.selectbox("Location", list(GEO_MAP.keys()) + ["Foreign_IP"], index=6)
        txn_stream = st.number_input("Stream ID", min_value=1, max_value=60, value=42)
    
    # Submit button for the form
    scan_button = st.form_submit_button("Run Deep Scan")

if scan_button:
    # 1. Construct the payload matching your Pydantic schema
    payload = {
        "transaction_id": f"MANUAL-{random.randint(1000, 9999)}",
        "user_id": "admin_investigator",
        "amount": txn_amount,
        "merchant_category": txn_category,
        "location": txn_location,
        "stream_id": txn_stream
    }
    
    # 2. Ping the FastAPI backend
    try:
        # Assuming your FastAPI is running locally on port 8000
        response = requests.post(API_URL, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            score = result.get("risk_score", 0.0)
            is_blocked = result.get("is_blocked", False)
            
            # 3. Render the Decision
            st.markdown("### Scan Results")
            if is_blocked:
                st.error(f"🚨 **FRAUD DETECTED** | Risk Score: {score:.4f} | Action: BLOCKED")
            else:
                st.success(f"✅ **TRANSACTION SAFE** | Risk Score: {score:.4f} | Action: APPROVED")
        else:
            st.warning(f"Backend API error: {response.status_code}. Ensure `python run.py` is active.")
            
    except requests.exceptions.ConnectionError:
        st.error("🔌 Connection Failed. Make sure your FastAPI backend (`python run.py`) is running in a separate terminal!")