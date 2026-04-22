import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="ATD Smart Calc", page_icon="⚡", layout="centered")

# --- CUSTOM CSS FOR DARK BLUE THEME ---
st.markdown("""
    <style>
    /* Main Background Dark Blue */
    .stApp {
        background-color: #001f3f; /* Deep Dark Blue */
        color: #ffffff;
    }

    /* Input Labels and Text Color */
    label, p, h1, h2, h3, .stMarkdown {
        color: #ffffff !important;
    }

    /* Metric Cards Styling */
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }

    /* Metric Value and Label Color */
    div[data-testid="stMetricValue"] > div {
        color: #00d4ff !important; /* Neon Blue for values */
    }
    div[data-testid="stMetricLabel"] > p {
        color: #cccccc !important;
    }

    /* Status Box for Tension Length */
    .status-box {
        padding: 10px;
        border-radius: 8px;
        background-color: rgba(0, 212, 255, 0.1);
        border-left: 4px solid #00d4ff;
        margin-bottom: 20px;
        font-size: 0.9em;
    }

    /* Minimalist Credit Section */
    .footer-credit {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        text-align: center;
        padding: 10px;
        font-size: 10px; /* Sabse chhota font */
        color: rgba(255, 255, 255, 0.4); /* Faded color */
        letter-spacing: 1px;
    }

    /* Divider color */
    hr {
        border-color: rgba(255, 255, 255, 0.1) !important;
    }
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
    except: return None

# --- HEADER (No Logos) ---
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
            L = float(df[df['Structure_No'] == selected_struct]['Tension_Length'].values[0])
            st.markdown(f"<div class='status-box'>Tension Length: {L} m</div>", unsafe_allow_html=True)
        else:
