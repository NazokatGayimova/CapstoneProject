import streamlit as st
import pandas as pd
from ai_query_agent import generate_sql_query, ask_database
from predict_trend import predict_air_quality_trend

# App Title
st.title("🌍 AI-Powered Air Quality Query Agent")
st.write("Enter your question about air quality data, and AI will generate an SQL query to fetch results.")

# User Query Input
user_query = st.text_input("🔎 Ask a question:", placeholder="What is the air quality in New York City?")

# Button to Run Query
if st.button("Run Query"):
    if user_query:
        sql_query = generate_sql_query(user_query)

        # Execute Query
        results = ask_database(sql_query)

        if isinstance(results, str) and "openweather.com" in results:
            st.warning("⚠️ No data found. Please visit [OpenWeather](https://openweather.com) for more information.")
        else:
            df = pd.DataFrame(results, columns=["Location", "PM2.5", "Year"])
            st.success("✅ Query executed successfully!")
            st.table(df)
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
