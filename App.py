import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(page_title="TRD Smart Calc | WR", page_icon="⚡", layout="centered")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-top: 5px solid #004182;
    }
    .credit-section {
        background-color: #004182;
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-top: 30px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .status-box {
        padding: 12px;
        border-radius: 8px;
        background-color: #e3f2fd;
        border-left: 5px solid #2196f3;
        margin-bottom: 20px;
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

# --- HEADER ---
st.image("https://upload.wikimedia.org/wikipedia/en/thumb/4/41/Indian_Railways_logo.svg/1200px-Indian_Railways_logo.svg.png", width=70)
st.title("OHE ATD Smart Calculator")
st.write("Western Railway | Traction Department")
st.markdown("---")

df = load_data()

# --- INPUT SECTION ---
col1, col2 = st.columns([1.5, 1])

with col1:
    if df is not None:
        struct_list = df['Structure_No'].dropna().unique().tolist()
        selected_struct = st.selectbox("📍 Select Structure Number", ["Manual Entry"] + struct_list)
        if selected_struct != "Manual Entry":
            L = float(df[df['Structure_No'] == selected_struct]['Tension_Length'].values[0])
            st.markdown(f"<div class='status-box'><b>Tension Length:</b> {L} m (Auto-fetched)</div>", unsafe_allow_html=True)
        else:
            L = st.number_input("Enter Length (L)", value=750.0)
    else:
        L = st.number_input("Enter Length (L)", value=750.0)

with col2:
    theta_2 = st.number_input("🌡️ Temp (°C)", value=35.0, step=0.5)

# --- CALCULATION ---
alpha = 0.000017
theta_1 = 35
delta_1 = L * alpha * (theta_1 - theta_2) * 1000
x_val = 1300 + delta_1
y_val = 2300 + (3 * delta_1)

# --- RESULTS ---
st.subheader("Field Results")
res1, res2 = st.columns(2)
res1.metric(label="X Value (Pulley)", value=f"{round(x_val, 1)} mm", delta=f"{round(delta_1, 1)} mm")
res2.metric(label="Y Value (Weight)", value=f"{round(y_val, 1)} mm", delta=f"{round(3*delta_1, 1)} mm")

# --- PERSONAL CREDIT SECTION ---
st.markdown(f"""
    <div class='credit-section'>
        <p style='margin:0; font-size: 0.9em; opacity: 0.8;'>Conceptualized & Developed by</p>
        <h3 style='margin:0; font-weight: bold;'>Akki (Junior Engineer)</h3>
        <p style='margin:0; font-size: 0.8em;'>Traction Department | Western Railway</p>
    </div>
    """, unsafe_allow_html=True)

# --- FOOTER ---
with st.expander("Technical Formula"):
    st.write("Standard Temperature: 35°C")
    st.latex(r"X = 1300 + [L \cdot \alpha \cdot (35 - t)]")
    st.latex(r"Y = 2300 + [3 \cdot \Delta_1]")
