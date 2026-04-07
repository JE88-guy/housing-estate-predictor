import streamlit as st
import joblib
import pandas as pd
import os

# 1. Robust Model Loading
path = 'Models/Population_Model.pkl'

if os.path.exists(path):
    model = joblib.load(path)
else:
    st.error(f"❌ Model file not found at {path}. Check your GitHub folder structure!")
    st.stop()

st.set_page_config(page_title="Housing Strategy", page_icon="🏠")
st.title("🏘️ Real Estate Strategy & Population Predictor")
st.markdown("---")

# 2. User Inputs (Matching your Training Features)
col1, col2 = st.columns(2)

with col1:
    target_year = st.selectbox("Target Year", [2025, 2026, 2027])
    pop_current = st.number_input("Current Population (Count)", value=1000000, step=10000)

with col2:
    growth_prev = st.slider("Previous Growth Rate (%)", 0.0, 5.0, 1.2)

# 3. Prediction Logic
if st.button("🚀 Analyze ROI Potential"):
    # Organize features into a list of lists (the "Shape" the model expects)
    # Ensure the order matches exactly: [Year, Prev_Population, Growth_Rate]
    input_data = [[target_year, pop_current, growth_prev]] 

    # Convert to DataFrame with the exact column names from your training
    feature_df = pd.DataFrame(input_data, columns=['Year', 'Prev_Population', 'Growth_Rate'])
    
    try:
        prediction = model.predict(feature_df)
        
        # Display Result
        st.write(f"### Projected {target_year} Population:")
        st.header(f"{int(prediction[0]):,}")
        
        # Strategy Logic
        if prediction[0] > 5000000:
            st.success("🎯 **High Priority:** Ideal for Large-Scale Housing Estates (Horizontal/Vertical Mix)")
        elif prediction[0] > 2000000:
            st.info("📈 **Moderate Priority:** Suitable for Mid-Sized Residential Subdivisions")
        else:
            st.warning("📉 **Strategic Caution:** Focus on Niche Developments or Commercial Units")
            
    except Exception as e:
        st.error(f"Model Error: {e}")
        st.info("Check if your model expects more/fewer features than provided.")
