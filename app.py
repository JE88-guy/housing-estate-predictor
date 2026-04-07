import streamlit as st
import joblib
import pandas as pd
import os

# 1. Load Model
path = 'Models/Population_Model.pkl'
if os.path.exists(path):
    model = joblib.load(path)
else:
    st.error("Model file not found! Ensure 'Models/Population_Model.pkl' is in your GitHub repo.")
    st.stop()

st.set_page_config(page_title="Housing Strategy", page_icon="🏠")
st.title("🏘️ Real Estate Strategy Predictor")

# 2. Define expected columns EXACTLY as the model saw them during training
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

# 3. Create Inputs (Defined OUTSIDE and BEFORE the button)
with st.sidebar:
    st.header("Input Parameters")
    target_year = st.selectbox("Target Year", [2025, 2026, 2027])
    
    # Use the specific regions the model expects
    regions_list = [
        'Cordillera Administrative Region (CAR)', 'National Capital Region (NCR)',
        'I - Ilocos Region', 'II - Cagayan Valley', 'III - Central Luzon',
        'CALABARZON', 'MIMAROPA Region', 'V - Bicol Region',
        'VI - Western Visayas', 'VII - Central Visayas', 'VIII - Eastern Visayas',
        'IX - Zamboanga Peninsula', 'X - Northern Mindanao', 'XI - Davao Region',
        'XII - SOCCSKSARGEN', '13 - Caraga', 'BARMM'
    ]
    selected_region = st.selectbox("Select Region", regions_list)

col1, col2 = st.columns(2)
with col1:
    pop_prev = st.number_input("Last Recorded Population", value=1000000)
    growth_prev = st.number_input("Last Recorded Growth Rate (%)", value=1.2)
with col2:
    pop_prev2 = st.number_input("Population (2 Years Ago)", value=980000)
    growth_prev2 = st.number_input("Growth Rate (2 Years Ago)", value=1.1)

# 4. Execution Logic
if st.button("Analyze ROI & Predict Population"):
    # Initialize all columns to 0
    input_dict = {col: [0] for col in expected_columns}
    
    # Fill numerical data
    input_dict['Year'] = [target_year]
    input_dict['Prev_Population'] = [pop_prev]
    input_dict['Prev2_Population'] = [pop_prev2]
    input_dict['Prev_Growth'] = [growth_prev]
    input_dict['Prev2_Growth'] = [growth_prev2]
    
    # Set the selected region to 1
    region_key = f"Region_{selected_region}"
    if region_key in input_dict:
        input_dict[region_key] = [1]
    
    # Create DataFrame and enforce column order
    feature_df = pd.DataFrame(input_dict)[expected_columns]
    
    try:
        prediction = model.predict(feature_df)
        result = int(prediction[0])
        
        st.divider()
        st.subheader(f"Results for {selected_region}")
        st.metric(label=f"Projected {target_year} Population", value=f"{result:,}")
        
        if result > 5000000:
            st.success("🎯 **High Priority:** High-density housing/Vertical development recommended.")
        elif result > 2000000:
            st.info("📈 **Moderate Priority:** Mid-sized residential subdivisions recommended.")
        else:
            st.warning("📉 **Niche Priority:** Focus on specialized or commercial units.")
            
    except Exception as e:
        st.error(f"Prediction Error: {e}")
