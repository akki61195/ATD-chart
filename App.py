import streamlit as st

# Page Configuration
st.set_page_config(page_title="ATD Calculator", page_icon="🚉")

st.title("🚉 Railway ATD X-Y Calculator")
st.write("Modified 3-Pulley (3:1 Ratio) - CAMTECH Formula")

# Input Section
st.subheader("Input Parameters")
col1, col2 = st.columns(2)

with col1:
    L = st.number_input("Tension Length (L) in meters", min_value=0.0, value=750.0, step=1.0)
    alpha = 0.000017  # Standard for Copper
    
with col2:
    theta_2 = st.number_input("Current Temperature (°C)", value=35.0, step=0.5)
    theta_1 = 35  # Standard Normal Temperature

# Calculation Logic
# 1. Expansion/Contraction (delta_1)
delta_1 = L * alpha * (theta_1 - theta_2) * 1000

# 2. X Value (Distance between pulleys)
x_val = 1300 + delta_1

# 3. Y Value (Distance between CW bottom and Muff top)
# For 3:1 ratio, movement is 3 times delta_1
y_val = 2300 + (3 * delta_1)

# Results Display
st.divider()
st.subheader("Calculated Results")
res_x, res_y = st.columns(2)

res_x.metric(label="X Value", value=f"{round(x_val, 1)} mm")
res_y.metric(label="Y Value", value=f"{round(y_val, 1)} mm")

# Technical Note
with st.expander("Formula Details"):
    st.write(f"Standard Temp: {theta_1}°C")
    st.write(f"Current Temp: {theta_2}°C")
    st.write(f"Delta-1 (Expansion): {round(delta_1, 2)} mm")
    st.latex(r"X = 1300 + \delta_1")
    st.latex(r"Y = 2300 + (3 \times \delta_1)")

st.info("Tip: Is portal ko mobile Chrome mein 'Add to Home Screen' karke app ki tarah use karein.")
