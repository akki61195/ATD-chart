import streamlit as st
import pandas as pd
import requests
import os

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="OHE ATD Smart Tool", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050a0f; color: white; }
    div[data-testid="stMetricValue"] > div { 
        color: #ffffff !important; 
        font-weight: 900 !important; 
        font-size: 38px !important; 
    }
    .scroll-container {
        width: 100%; overflow: hidden; background-color: #050a0f;
        border-top: 1px solid #30363d; position: fixed; bottom: 0; left: 0;
        padding: 5px 0; z-index: 1000;
    }
    .scroll-text {
        display: inline-block; white-space: nowrap; font-size: 14px;
        font-weight: bold; color: #00d4ff; animation: marquee 15s linear infinite;
    }
    @keyframes marquee { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SMART DATA LOADING (Online/Offline) ---
SHEET_ID = "1vfioGSmpC7a5S8SMUpCk9xn-mtttvcTecLEQ1Sd6XkU"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=xlxs"
LOCAL_FILE = "atd_data.csv"

@st.cache_data
def load_data():
    # Pehle Online check karega
    try:
        df = pd.read_csv(SHEET_URL, timeout=3)
        df.columns = df.columns.str.strip()
        # Naya data milte hi local mein save kar lega (future offline ke liye)
        df.to_csv(LOCAL_FILE, index=False)
        return df, "Online (Latest)"
    except:
        # Agar net nahi hai toh local CSV uthayega
        if os.path.exists(LOCAL_FILE):
            df = pd.read_csv(LOCAL_FILE)
            df.columns = df.columns.str.strip()
            return df, "Offline (Local CSV)"
        else:
            return None, "No Data Found"

# --- 3. UI ---
st.markdown("<h2 style='text-align: center; color: #00d4ff;'>OHE ATD Smart Tool</h2>", unsafe_allow_html=True)

df, status = load_data()
st.caption(f"Status: {status}")

if df is not None:
    struct_list = df['Structure_No'].dropna().unique().tolist()
    selected_struct = st.selectbox("📍 Select Structure No", ["Manual Entry"] + struct_list)
    
    if selected_struct != "Manual Entry":
        L = float(df[df['Structure_No'] == selected_struct]['Tension_Length'].values[0])
        st.info(f"Tension Length (L): {L} m")
    else:
        L = st.number_input("Enter Tension Length (L) manually", value=750.0)
else:
    L = st.number_input("CSV/Sheet missing. Enter L manually", value=750.0)

# --- 4. CALCULATION ---
theta_2 = st.number_input("Current Temp (°C)", value=35.0, step=0.1)

# Formula
delta = L * 0.000017 * (35 - theta_2) * 1000
x_val, y_val = 1300 + delta, 2300 + (3 * delta)

st.divider()
c1, c2 = st.columns(2)
c1.metric("X (Pulley Gap)", f"{round(x_val, 1)} mm")
c2.metric("Y (Weight Height)", f"{round(y_val, 1)} mm")

# --- 5. SCROLLING FOOTER ---
st.markdown(f"""
    <div class="scroll-container">
        <div class="scroll-text">
            DEVELOPED BY: A.K.MULCHANDANI JE/TRD (TRACTION DEPARTMENT) - INDIAN RAILWAYS --- ⚡ RAILWAY ENGINEERING ⚡
        </div>
    </div>
""", unsafe_allow_html=True)
