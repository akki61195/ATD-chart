import streamlit as st
import pandas as pd
import requests
import os

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="OHE ATD Smart Tool", page_icon="⚡")

st.markdown("""
    <style>
    .stApp { background-color: #050a0f; color: white; }
    .stMetricValue { color: white !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA LOADING LOGIC ---
SHEET_ID = "1vfioGSmpC7a5S8SMUpCk9xn-mtttvcTecLEQ1Sd6XkU"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
LOCAL_FILE = "atd_data.csv"

def load_data():
    # Priority 1: Try Online
    try:
        df = pd.read_csv(SHEET_URL, timeout=2)
        df.columns = df.columns.str.strip()
        df.to_csv(LOCAL_FILE, index=False) # Auto-save for offline
        return df, "✅ Online Mode"
    except:
        # Priority 2: Try Local Folder
        if os.path.exists(LOCAL_FILE):
            df = pd.read_csv(LOCAL_FILE)
            return df, "📶 Offline Mode (Saved Data)"
        return None, "❌ Data Not Found"

st.title("OHE ATD Smart Tool")

# --- 3. UPLOAD SECTION (If file is missing) ---
df, status = load_data()

if df is None:
    st.warning("Data file nahi mili. Please apni CSV file upload karein.")
    uploaded_file = st.file_uploader("Choose CSV file", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        df.to_csv(LOCAL_FILE, index=False) # Save it for next time
        st.success("File uploaded successfully!")
        st.rerun()
else:
    st.caption(f"Status: {status}")

# --- 4. CALCULATION INTERFACE ---
if df is not None:
    struct_list = df['Structure_No'].dropna().unique().tolist()
    selected_struct = st.selectbox("📍 Select Structure No", ["Manual Entry"] + struct_list)
    
    if selected_struct != "Manual Entry":
        L = float(df[df['Structure_No'] == selected_struct]['Tension_Length'].values[0])
        st.write(f"**Tension Length (L):** {L} m")
    else:
        L = st.number_input("Enter Tension Length (L) manually", value=750.0)
    
    temp = st.number_input("Current Temp (°C)", value=35.0, step=0.1)
    
    # Standard Railway Formula
    delta = L * 0.000017 * (35 - temp) * 1000
    x_val = 1300 + delta
    y_val = 2300 + (3 * delta)
    
    st.divider()
    c1, c2 = st.columns(2)
    c1.metric("X (Pulley Gap)", f"{round(x_val, 1)} mm")
    c2.metric("Y (Weight Height)", f"{round(y_val, 1)} mm")

st.markdown("---")
st.caption("Developed by A.K. Mulchandani JE/TRD")
