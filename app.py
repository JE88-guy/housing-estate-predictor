import streamlit as st
import joblib
import pandas as pd
import os

# 1. Load Model
path = 'Models/Population_Model.pkl'
if os.path.exists(path):
    model = joblib.load(path)
    # Get the exact list of features the model was trained on
    try:
        model_features = model.feature_names_in_.tolist()
    except AttributeError:
        st.error("This model doesn't have feature names saved. Please re-save it in Colab using a DataFrame.")
        st.stop()
else:
    st.error("Model file not found! Check your GitHub folder.")
    st.stop()

st.title("🏠 Housing Estate Strategy Predictor")

# 2. Setup Input Fields
with st.sidebar:
    st.header("Settings")
    target_year = st.selectbox("Year", [2025, 2026, 2027])
    
    # Let's extract region names from the model's features automatically!
    # This looks for any feature starting with 'Region_'
    available_regions = [f.replace('Region_', '') for f in model_features if f.startswith('Region_')]
    selected_region_name = st.selectbox("Select Region", available_regions)

col1, col2 = st.columns(2)
with col1:
    pop_prev = st.number_input("Last Population", value=1000000)
    growth_prev = st.number_input("Last Growth Rate (%)", value=1.2)
with col2:
    pop_prev2 = st.number_input("Population (2 yrs ago)", value=980000)
    growth_prev2 = st.number_input("Growth Rate (2 yrs ago)", value=1.1)

# 3. Prediction Logic
if st.button("Analyze Strategy"):
    # Create a dictionary with ALL features the model expects, initialized to 0
    input_dict = {col: [0.0] for col in model_features}
    
    # Fill in the numerical values (using exact model names)
    if 'Year' in input_dict: input_dict['Year'] = [float(target_year)]
    if 'Prev_Population' in input_dict: input_dict['Prev_Population'] = [float(pop_prev)]
    if 'Prev2_Population' in input_dict: input_dict['Prev2_Population'] = [float(pop_prev2)]
    if 'Prev_Growth' in input_dict: input_dict['Prev_Growth'] = [float(growth_prev)]
    if 'Prev2_Growth' in input_dict: input_dict['Prev2_Growth'] = [float(growth_prev2)]
    
    # 4. Handle 'Rolling Growth' (Calculation)
    if 'Rolling Growth' in input_dict:
        input_dict['Rolling Growth'] = [(float(growth_prev) + float(growth_prev2)) / 2]
    
    # 5. Handle the Region (The "One-Hot" bit)
    region_column = f"Region_{selected_region_name}"
    if region_column in input_dict:
        input_dict[region_column] = [1.0]
    
    # Convert to DataFrame and predict
    feature_df = pd.DataFrame(input_dict)[model_features]
    
    try:
        prediction = model.predict(feature_df)
        st.divider()
        st.metric(f"Projected {target_year} Population", f"{int(prediction[0]):,}")
        st.success("Analysis Complete!" if prediction[0] > 5000000 else "Moderate growth detected.")
    except Exception as e:
        st.error(f"Prediction Error: {e}")

# DEBUG TOOLS (Expand this if you get stuck again)
with st.expander("🛠️ Debug: See Model's Required Features"):
    st.write("Your model expects these exact columns:")
    st.write(model_features)
