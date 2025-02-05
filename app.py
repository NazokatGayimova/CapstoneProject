import streamlit as st
import pandas as pd
from ai_query_agent import handle_query
from predict_trend import predict_air_quality_trend

st.title("🌍 AI-Powered Air Quality Query Agent")

st.write("Enter your question about air quality data, and AI will generate a response.")

# User input field
user_query = st.text_input("🔎 Ask a question:", placeholder="What is the air quality in New York City?")

if st.button("Run Query"):
    if user_query:
        result = handle_query(user_query)

        if isinstance(result, dict):
            st.success(f"✅ Real-time Air Quality for {result['location']}")
            st.write(f"**AQI Level:** {result['aqi']}")
            st.write("**Pollutants:**")
            for pollutant, value in result["pollutants"].items():
                st.write(f"- {pollutant}: {value}")
        elif isinstance(result, str):
            st.write(result)  # Display AI response (e.g., prediction, OpenWeather redirection)
        else:
            st.error("⚠️ Unexpected response from AI query agent.")
    else:
        st.error("⚠️ Please enter a question.")

# Air Quality Prediction Section
st.header("📈 Predict Future Air Quality Trends")

location_input = st.text_input("🌍 Enter a location:", placeholder="e.g., London")

if st.button("Predict Trend"):
    if location_input:
        prediction = predict_air_quality_trend(location_input)
        st.write(prediction)
    else:
        st.error("⚠️ Please enter a location.")
