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

# 1. The EXACT column names the model is looking for
expected_columns = [
    'Prev2_Growth', 'Prev2_Population', 'Prev_Growth', 'Prev_Population', 'Year',
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

# 2. The display names for your dropdown (mapped to the keys above)
regions_map = {
    'Ilocos Region': 'Region I (Ilocos Region)',
    'Cagayan Valley': 'Region II (Cagayan Valley)',
    'Central Luzon': 'Region III (Central Luzon)',
    'CALABARZON': 'Region IV-A (CALABARZON)',
    'MIMAROPA': 'Region IV-B (MIMAROPA)',
    'Bicol Region': 'Region V (Bicol Region)',
    'Western Visayas': 'Region VI (Western Visayas)',
    'Central Visayas': 'Region VII (Central Visayas)',
    'Eastern Visayas': 'Region VIII (Eastern Visayas)',
    'Zamboanga Peninsula': 'Region IX (Zamboanga Peninsula)',
    'Northern Mindanao': 'Region X (Northern Mindanao)',
    'Davao Region': 'Region XI (Davao Region)',
    'SOCCSKSARGEN': 'Region XII (SOCCSKSARGEN)',
    'Caraga': 'Region XIII (Caraga)',
    'ARMM': 'Autonomous Region in Muslim Mindanao (ARMM)',
    'CAR': 'Cordillera Administrative Region (CAR)',
    'NCR': 'National Capital Region (NCR)'
}

# Update your Sidebar code:
with st.sidebar:
    selected_display_name = st.selectbox("Select Region", list(regions_map.keys()))
    # This gets the "Internal" name the model needs
    selected_region = regions_map[selected_display_name] 

# The rest of the logic (input_dict and feature_df) remains the same!
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
