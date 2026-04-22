import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="ATD Smart Calc", page_icon="⚡", layout="centered")

# --- CUSTOM CSS FOR DARK BLUE THEME ---
st.markdown("""
    <style>
    .stApp {
        background-color: #001f3f;
        color: #ffffff;
    }
    label, p, h1, h2, h3, .stMarkdown {
        color: #ffffff !important;
    }
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 10px;
    }
    div[data-testid="stMetricValue"] > div {
        color: #00d4ff !important;
    }
    .status-box {
        padding: 10px;
        border-radius: 8px;
        background-color: rgba(0, 212, 255, 0.1);
        border-left: 4px solid #00d4ff;
        margin-bottom: 20px;
    }
    .footer-credit {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        text-align: center;
        padding: 10px;
        font-size: 10px;
        color: rgba(255, 255, 255, 0.4);
    }
    hr { border-color: rgba(255, 255, 255, 0.1) !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA LOADING ---
SHEET_ID = "1vfioGSmpC7a5S8SMUpCk9xn-mtttvcTecLEQ1Sd6XkU"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = df.columns.str.strip() 
        return df
    except:
        return None

# --- HEADER ---
st.markdown("<h2 style='text-align: center;'>OHE ATD Smart Calculator</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; opacity: 0.7;'>Precision Engineering Tool</p>", unsafe_allow_html=True)
st.markdown("---")

df = load_data()

# --- INPUT SECTION ---
col1, col2 = st.columns([1.5, 1])

with col1:
    if df is not None:
        struct_list = df['Structure_No'].dropna().unique().tolist()
        selected_struct = st.selectbox("📍 Structure Number", ["Manual Entry"] + struct_list)
        if selected_struct != "Manual Entry":
            L_val = df[df['Structure_No'] == selected_struct]['Tension_Length'].values[0]
            L = float(L_val)
            st.markdown(f"<div class='status-box'>Tension Length: {L} m</div>", unsafe_allow_html=True)
        else:
            L = st.number_input("Manual Tension Length (L)", value=750.0)
    else:
        L = st.number_input("Tension Length (L)", value=750.0)

with col2:
    theta_2 = st.number_input("🌡️ Current Temp (°C)", value=35.0, step=0.5)

# --- CALCULATIONS ---
try:
    alpha, theta_1 = 0.000017, 35
    delta_1 = float(L) * alpha * (theta_1 - float(theta_2)) * 1000
    x_val = 1300 + delta_1
    y_val = 2300 + (3 * delta_1)

    # --- RESULTS ---
    st.write("#### Technical Output")
    r1, r2 = st.columns(2)
    r1.metric(label="X Value (Pulley)", value=f"{round(x_val, 1)} mm", delta=f"{round(delta_1, 1)} mm")
    r2.metric(label="Y Value (Weight)", value=f"{round(y_val, 1)} mm", delta=f"{round(3*delta_1, 1)} mm")

except Exception as e:
    st.error("Data check karein. Calculation mein problem hai.")

# --- MINIMALIST CREDIT ---
st.markdown("<div class='footer-credit'>DEVELOPED BY: A.K.MULCHANDANI JE/TRD</div>", unsafe_allow_html=True)
