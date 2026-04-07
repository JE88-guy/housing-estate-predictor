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
expected_columns = [
    'Prev2_Growth', 'Prev2_Population', 'Prev_Growth', 'Prev_Population', 'Year',
    'Region_Cordillera Administrative Region (CAR)',
    'Region_National Capital Region (NCR)',
    'Region_I - Ilocos Region', 'Region_II - Cagayan Valley', 
    'Region_III - Central Luzon', 'Region_CALABARZON', 
    'Region_MIMAROPA Region', 'Region_V - Bicol Region',
    'Region_VI - Western Visayas', 'Region_VII - Central Visayas', 
    'Region_VIII - Eastern Visayas', 'Region_IX - Zamboanga Peninsula', 
    'Region_X - Northern Mindanao', 'Region_XI - Davao Region',
    'Region_XII - SOCCSKSARGEN', 'Region_13 - Caraga', 'Region_BARMM'
]

if st.button("Analyze Strategy"):
    # Create a dictionary with ALL columns initialized to 0
    input_dict = {col: [0] for col in expected_columns}
    
    # Fill in the numerical values
    input_dict['Year'] = [target_year]
    input_dict['Prev_Population'] = [pop_prev]
    input_dict['Prev2_Population'] = [pop_prev2]
    input_dict['Prev_Growth'] = [growth_prev]
    input_dict['Prev2_Growth'] = [growth_prev2]
    
    # Fill in the One-Hot Region (The "1")
    region_col = f"Region_{selected_region}"
    if region_col in input_dict:
        input_dict[region_col] = [1]
    
    # Convert to DataFrame - this maintains the EXACT order of expected_columns
    feature_df = pd.DataFrame(input_dict)[expected_columns]
    
    try:
        prediction = model.predict(feature_df)
        st.header(f"Projected Population: {int(prediction[0]):,}")
    except Exception as e:
        st.error(f"Alignment Error: {e}")
