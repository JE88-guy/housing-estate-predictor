import streamlit as st
import joblib
import pandas as pd

# Load your model (Make sure the path matches your Drive!)
path = '/content/drive/MyDrive/Models/Population_Model.pkl'
model = joblib.load(path)

st.set_page_config(page_title="Housing Strategy", page_icon="🏠")
st.title("Real Estate Strategy & Population Predictor")

# Input features based on your Phase 4 model
# Adjust these based on your actual feature names!
pop_2024 = st.number_input("Enter 2024 Population", value=1000000)
growth_prev = st.slider("Previous Growth Rate (%)", 0.0, 5.0, 1.2)

if st.button("Analyze ROI Potential"):
    # This must match the shape of your 'features' variable from Phase 5
    features = [[pop_2024, growth_prev]]
    prediction = model.predict(features)

    st.write(f"### Projected 2025 Population: {int(prediction[0]):,}")

    if prediction[0] > 5000000:
        st.success("🎯 High Priority: Ideal for Large-Scale Housing Estates")
    else:
        st.info("📉 Moderate Priority: Focus on Niche Developments")