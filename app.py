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

# 2. EXACT Columns from your Model's Memory
expected_columns = [
    'Prev2_Growth', 'Prev2_Population', 'Prev_Growth', 'Prev_Population', 
    'Rolling Growth', 'Year', 
    'Region_Cordillera Administrative Region (CAR)',
    'Region_National Capital Region (NCR)',
    'Region_Region I (Ilocos Region)', 
    'Region_Region II (Cagayan Valley)', 
    'Region_Region III (Central Luzon)', 
    'Region_Region IV-A (CALABARZON)', 
    'Region_Region IV-B (MIMAROPA)',
    'Region_Region V (Bicol Region)',
    'Region_Region VI (Western Visayas)',
    'Region_Region VII (Central Visayas)',
    'Region_Region VIII (Eastern Visayas)',
    'Region_Region IX (Zamboanga Peninsula)',
    'Region_Region X (Northern Mindanao)',
    'Region_Region XI (Davao Region)',
    'Region_Region XII (SOCCSKSARGEN)',
    'Region_Region XIII (Caraga)',
    'Region_Autonomous Region in Muslim Mindanao (ARMM)'
]

# 3. Correct Region Mapping
regions_map = {
    'NCR': 'Region_National Capital Region (NCR)',
    'CAR': 'Region_Cordillera Administrative Region (CAR)',
    'Ilocos Region': 'Region_Region I (Ilocos Region)',
    'Cagayan Valley': 'Region_Region II (Cagayan Valley)',
    'Central Luzon': 'Region_Region III (Central Luzon)',
    'CALABARZON': 'Region_Region IV-A (CALABARZON)',
    'MIMAROPA': 'Region_Region IV-B (MIMAROPA)',
    'Bicol Region': 'Region_Region V (Bicol Region)',
    'Western Visayas': 'Region_Region VI (Western Visayas)',
    'Central Visayas': 'Region_Region VII (Central Visayas)',
    'Eastern Visayas': 'Region_Region VIII (Eastern Visayas)',
    'Zamboanga Peninsula': 'Region_Region IX (Zamboanga Peninsula)',
    'Northern Mindanao': 'Region_Region X (Northern Mindanao)',
    'Davao Region': 'Region_Region XI (Davao Region)',
    'SOCCSKSARGEN': 'Region_Region XII (SOCCSKSARGEN)',
    'Caraga': 'Region_Region XIII (Caraga)',
    'ARMM': 'Region_Autonomous Region in Muslim Mindanao (ARMM)'
}

# 4. Inputs
with st.sidebar:
    st.header("Parameters")
    target_year = st.selectbox("Year", [2025, 2026, 2027])
    selected_display = st.selectbox("Select Region", list(regions_map.keys()))

col1, col2 = st.columns(2)
with col1:
    pop_prev = st.number_input("Last Recorded Population", value=1000000)
    growth_prev = st.number_input("Last Growth Rate (%)", value=1.2)
with col2:
    pop_prev2 = st.number_input("Population (2 Years Ago)", value=980000)
    growth_prev2 = st.number_input("Growth Rate (2 Years Ago)", value=1.1)

# 5. Prediction Logic (ONLY ONE BUTTON CALL HERE)
if st.button("Analyze Strategy", key="main_prediction_btn"):
    input_dict = {col: [0.0] for col in expected_columns}
    
    # Fill Numerical Data
    input_dict['Year'] = [float(target_year)]
    input_dict['Prev_Population'] = [float(pop_prev)]
    input_dict['Prev2_Population'] = [float(pop_prev2)]
    input_dict['Prev_Growth'] = [float(growth_prev)]
    input_dict['Prev2_Growth'] = [float(growth_prev2)]
    
    # Calculate Rolling Growth (Required Feature)
    input_dict['Rolling Growth'] = [(float(growth_prev) + float(growth_prev2)) / 2]
    
    # Map Region
    region_column = regions_map[selected_display]
    if region_column in input_dict:
        input_dict[region_column] = [1.0]
    
    # Predict
    feature_df = pd.DataFrame(input_dict)[expected_columns]
    
    try:
        prediction = model.predict(feature_df)
        result = int(prediction[0])
        st.divider()
        st.metric(label=f"Projected {target_year} Population", value=f"{result:,}")
        
        if result > 5000000:
            st.success("🎯 **High Priority:** Large-scale housing potential.")
        else:
            st.info("📉 **Selective Priority:** Niche market focus.")
    except Exception as e:
        st.error(f"Prediction Error: {e}")
