import streamlit as st
import pandas as pd
import requests
import os

# --- 1. PAGE SETUP & BRIGHT WHITE CSS ---
st.set_page_config(page_title="OHE ATD Smart Tool", page_icon="⚡")

st.markdown("""
    <style>
    .stApp { background-color: #050a0f; color: white; }
    
    /* X and Y Values - Super Bright White */
    div[data-testid="stMetricValue"] > div { 
        color: #ffffff !important; 
        font-weight: 900 !important; 
        font-size: 45px !important; 
        text-shadow: 0px 0px 15px rgba(255, 255, 255, 0.8), 2px 2px 4px #000000;
    }
    
    /* Labels Brightness */
    div[data-testid="stMetricLabel"] > div > p {
        color: #00d4ff !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }

    /* Fixed Center Credit at Bottom */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 80%;
        background-color: #050a0f;
        color: #00d4ff;
        text-align: center;
        padding: 08px;
        font-weight: bold;
        border-top: 0.5px solid #30363d;
        z-index: 100;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SMART DATA LOADING (ONLINE/OFFLINE) ---
SHEET_ID = "1vfioGSmpC7a5S8SMUpCk9xn-mtttvcTecLEQ1Sd6XkU"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
LOCAL_FILE = "atd_data.csv"

@st.cache_data(ttl=60) # Har 1 min baad naya data check karega
def load_data():
    # Try Online First
    try:
        response = requests.get(SHEET_URL, timeout=2) # 2 sec wait karega
        if response.status_code == 200:
            df = pd.read_csv(SHEET_URL)
            df.columns = df.columns.str.strip()
            df.to_csv(LOCAL_FILE, index=False) # Offline ke liye save karega
            return df, "🌐 ONLINE MODE (Latest Data)"
    except:
        pass
    
    # Fallback to Offline
    if os.path.exists(LOCAL_FILE):
        df = pd.read_csv(LOCAL_FILE)
        df.columns = df.columns.str.strip()
        return df, "📶 OFFLINE MODE (Using Saved CSV)"
    
    return None, "❌ NO DATA FOUND (Connect Internet Once)"

# --- 3. UI MAIN ---
st.markdown("<h2 style='text-align: center; color: #00d4ff;'>OHE ATD Smart Tool</h2>", unsafe_allow_html=True)

df, status_msg = load_data()
st.sidebar.markdown(f"**Status:** {status_msg}")

if df is not None:
    struct_list = df['Structure_No'].dropna().unique().tolist()
    selected_struct = st.selectbox("📍 Select Structure No", ["Manual Entry"] + struct_list)
    
    if selected_struct != "Manual Entry":
        L = float(df[df['Structure_No'] == selected_struct]['Tension_Length'].values[0])
        st.markdown(f"<h3 style='color: #00ff41;'>Tension Length (L): {L} m</h3>", unsafe_allow_html=True)
    else:
        L = st.number_input("Enter L manually", value=750.0)
    
    temp = st.number_input("Current Temp (°C)", value=35.0, step=0.1)
    
    # Formula
    delta = L * 0.000017 * (35 - temp) * 1000
    x_val = 1300 + delta
    y_val = 2300 + (3 * delta)
    
    st.divider()
    col1, col2 = st.columns(2)
    col1.metric("X (PULLEY GAP)", f"{round(x_val, 1)} mm")
    col2.metric("Y (WEIGHT HEIGHT)", f"{round(y_val, 1)} mm")

else:
    st.error("Data Load nahi ho paya. Ek baar internet on karke app refresh karein.")

# --- 4. CENTERED FOOTER ---
st.markdown(f"""
    <div class="footer">
        DEVELOPED BY: A.K.MULCHANDANI JE/TRD (TRACTION DEPARTMENT)
    </div>
    """, unsafe_allow_html=True)
