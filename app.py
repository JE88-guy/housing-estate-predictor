import streamlit as st
import joblib
import pandas as pd
import numpy as np

# Load Model
path = 'Models/Population_Model.pkl'
model = joblib.load(path)

st.title("🏘️ Housing Estate Strategy Predictor")

# 1. User Inputs
target_year = st.selectbox("Year", [2025, 2026, 2027])
pop_prev = st.number_input("Previous Population", value=1000000)
pop_prev2 = st.number_input("Population (2 Years Ago)", value=980000)
growth_prev = st.number_input("Previous Growth Rate", value=1.2)
growth_prev2 = st.number_input("Growth Rate (2 Years Ago)", value=1.1)

# List ALL regions exactly as they appeared in your training data
regions = [
    'National Capital Region (NCR)', 
    'Cordillera Administrative Region (CAR)',
    'I - Ilocos Region', 'II - Cagayan Valley', 'III - Central Luzon',
    'CALABARZON', 'MIMAROPA Region', 'V - Bicol Region',
    'VI - Western Visayas', 'VII - Central Visayas', 'VIII - Eastern Visayas',
    'IX - Zamboanga Peninsula', 'X - Northern Mindanao', 'XI - Davao Region',
    'XII - SOCCSKSARGEN', '13 - Caraga', 'BARMM'
]
selected_region = st.selectbox("Select Region", regions)

if st.button("Analyze Strategy"):
    # 2. Create the base features (Numerical)
    # Order must match your error: Prev2_Growth, Prev2_Population, Prev_Growth, Prev_Population, Year
    data = {
        'Prev2_Growth': [growth_prev2],
        'Prev2_Population': [pop_prev2],
        'Prev_Growth': [growth_prev],
        'Prev_Population': [pop_prev],
        'Year': [target_year]
    }
    
    # 3. Handle One-Hot Encoding for Regions
    for reg in regions:
        column_name = f"Region_{reg}"
        data[column_name] = [1 if reg == selected_region else 0]
    
    # 4. Convert to DataFrame
    feature_df = pd.DataFrame(data)
    
    # 5. Predict
    prediction = model.predict(feature_df)
    
    st.header(f"Projected Population: {int(prediction[0]):,}")
    
    # Strategy Logic
    if prediction[0] > 5000000:
        st.success("🎯 **High Priority:** High-density housing recommended.")
    else:
        st.info("📉 **Moderate Priority:** Focused development recommended.")
