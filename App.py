import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(page_title="Smart ATD Calc", page_icon="🚉")

# Google Sheet CSV Link
SHEET_ID = "1vfioGSmpC7a5S8SMUpCk9xn-mtttvcTecLEQ1Sd6XkU"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        return df
    except Exception as e:
        return None

# App UI
st.title("🚉 Smart ATD X-Y Calculator")
st.write("Modified 3-Pulley (3:1) - Asset Linked")

df = load_data()

# Input Section
st.subheader("Asset & Environment")
col1, col2 = st.columns(2)

with col1:
    if df is not None:
        # Structure Selection from Sheet
        struct_list = df['Structure_No'].dropna().unique().tolist()
        selected_struct = st.selectbox("Select Structure No:", ["Manual Entry"] + struct_list)
        
        if selected_struct != "Manual Entry":
            L = df[df['Structure_No'] == selected_struct]['Tension_Length'].values[0]
            st.success(f"Tension Length: {L}m (Auto-fetched)")
        else:
            L = st.number_input("Enter Tension Length (L) manually:", value=750.0)
    else:
        st.error("Sheet connect nahi ho saki. Manual entry karein.")
        L = st.number_input("Enter Tension Length (L):", value=750.0)

with col2:
    theta_2 = st.number_input("Current Temperature (°C)", value=35.0, step=0.5)

# Calculation Logic
alpha = 0.000017
theta_1 = 35
delta_1 = L * alpha * (theta_1 - theta_2) * 1000
x_val = 1300 + delta_1
y_val = 2300 + (3 * delta_1)

# Results
st.divider()
res1, res2 = st.columns(2)
res1.metric("X Value (Pulley)", f"{round(x_val, 1)} mm")
res2.metric("Y Value (Weight)", f"{round(y_val, 1)} mm")

st.info
