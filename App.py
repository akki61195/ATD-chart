import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Smart ATD Calc", page_icon="🚉")

# Google Sheet CSV Link
SHEET_ID = "1vfioGSmpC7a5S8SMUpCk9xn-mtttvcTecLEQ1Sd6XkU"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        # Column names se extra space hatane ke liye
        df.columns = df.columns.str.strip() 
        return df
    except Exception as e:
        return None

# App Title
st.title("🚉 Smart ATD X-Y Calculator")
st.write("Modified 3-Pulley (3:1 Ratio) - CAMTECH Formula")

df = load_data()

# Input Section
st.subheader("Asset & Environment")
col1, col2 = st.columns(2)

with col1:
    if df is not None:
        # Check if 'Structure_No' exists in sheet
        if 'Structure_No' in df.columns:
            struct_list = df['Structure_No'].dropna().unique().tolist()
            selected_struct = st.selectbox("Select Structure No:", ["Manual Entry"] + struct_list)
            
            if selected_struct != "Manual Entry":
                # Fetching L and converting to float safely
                L_raw = df[df['Structure_No'] == selected_struct]['Tension_Length'].values[0]
                L = float(L_raw)
                st.success(f"Tension Length: {L}m (Auto-fetched)")
            else:
                L = st.number_input("Enter Tension Length (L):", value=750.0)
        else:
            st.error("Sheet mein 'Structure_No' column nahi mila.")
            L = st.number_input("Enter Tension Length (L):", value=750.0)
    else:
        st.error("Sheet connect nahi ho saki.")
        L = st.number_input("Enter Tension Length (L):", value=750.0)

with col2:
    theta_2 = st.number_input("Current Temperature (°C)", value=35.0, step=0.5)

# Calculation Logic (Safe Conversion)
try:
    alpha = 0.000017
    theta_1 = 35
    
    # Final Formula
    delta_1 = float(L) * alpha * (theta_1 - float(theta_2)) * 1000
    x_val = 1300 + delta_1
    y_val = 2300 + (3 * delta_1)

    # Results Display
    st.divider()
    res1, res2 = st.columns(2)
    
    res1.metric(label="X Value (Pulley)", value=f"{round(x_val, 1)} mm")
    res2.metric(label="Y Value (Weight)", value=f"{round(y_val, 1)} mm")

    # Technical Details Expander
    with st.expander("Formula & Calculations"):
        st.write(f"Standard Temp: {theta_1}°C")
        st.write(f"Delta-1: {round(delta_1, 2)} mm")
        st.latex(r"X = 1300 + \delta_1")
        st.latex(r"Y = 2300 + (3 \times \delta_1)")

except Exception as calc_error:
    st.error(f"Calculation Error: {calc_error}")

st.info("Tip: Naya structure add karne ke liye bas Google Sheet update karein.")
