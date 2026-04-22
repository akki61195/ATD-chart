import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(page_title="WR ATD Smart Calc", page_icon="🚉", layout="centered")

# --- CUSTOM CSS WITH BACKGROUND LOGO ---
st.markdown("""
    <style>
    /* Background Logo Effect */
    .stApp {
        background-image: url("https://upload.wikimedia.org/wikipedia/en/thumb/4/41/Indian_Railways_logo.svg/1200px-Indian_Railways_logo.svg.png");
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
        background-size: 400px; /* Logo size in background */
        opacity: 0.95; /* Overall app opacity */
    }

    /* Overlay to make text readable */
    .stApp::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(245, 247, 249, 0.92); /* Background tint to keep it clean */
        z-index: -1;
    }

    .stMetric {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        border-top: 5px solid #004182;
    }

    .credit-section {
        background: linear-gradient(90deg, #004182, #0056b3);
        color: white;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        margin-top: 30px;
        box-shadow: 0 4px 15px rgba(0,65,130,0.3);
    }

    .status-box {
        padding: 12px;
        border-radius: 10px;
        background-color: rgba(227, 242, 253, 0.8);
        border-left: 5px solid #2196f3;
        font-weight: 500;
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

# --- HEADER SECTION ---
col_logo, col_title = st.columns([1, 4])
with col_logo:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/4/41/Indian_Railways_logo.svg/1200px-Indian_Railways_logo.svg.png", width=80)
with col_title:
    st.title("Western Railway")
    st.subheader("OHE ATD Smart Calculator")

st.markdown("---")

df = load_data()

# --- INPUT SECTION ---
with st.container():
    c1, c2 = st.columns([1.5, 1])
    with c1:
        if df is not None:
            struct_list = df['Structure_No'].dropna().unique().tolist()
            selected_struct = st.selectbox("📍 Structure Number Selection", ["Manual Entry"] + struct_list)
            if selected_struct != "Manual Entry":
                L = float(df[df['Structure_No'] == selected_struct]['Tension_Length'].values[0])
                st.markdown(f"<div class='status-box'>Tension Length: {L} m</div>", unsafe_allow_html=True)
            else:
                L = st.number_input("Manual Tension Length (L)", value=750.0)
        else:
            L = st.number_input("Tension Length (L)", value=750.0)
    with c2:
        theta_2 = st.number_input("🌡️ Current Temp (°C)", value=35.0, step=0.5)

# --- CALCULATIONS ---
alpha, theta_1 = 0.000017, 35
delta_1 = L * alpha * (theta_1 - theta_2) * 1000
x_val, y_val = 1300 + delta_1, 2300 + (3 * delta_1)

# --- RESULTS ---
st.write("### Technical Field Parameters")
r1, r2 = st.columns(2)
r1.metric(label="X Value (Pulley)", value=f"{round(x_val, 1)} mm", delta=f"{round(delta_1, 1)} mm")
r2.metric(label="Y Value (Weight)", value=f"{round(y_val, 1)} mm", delta=f"{round(3*delta_1, 1)} mm")

# --- BRANDING / CREDIT ---
st.markdown(f"""
    <div class='credit-section'>
        <p style='margin:0; font-size: 0.85em; letter-spacing: 1px;'>CONCEPTUALIZED & DEVELOPED BY</p>
        <h2 style='margin:5px 0; color: #FFD700;'>Akki</h2>
        <p style='margin:0; font-weight: 500;'>Junior Engineer | Traction Department</p>
        <p style='margin:0; font-size: 0.8em; opacity: 0.9;'>Western Railway, Gujarat</p>
    </div>
    """, unsafe_allow_html=True)
