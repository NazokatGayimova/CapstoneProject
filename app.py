import streamlit as st
import sqlite3
from ai_query_agent import generate_sql_query, ask_database
from predict_trend import predict_air_quality_trend

st.title("\U0001F30D AI-Powered Air Quality Query Agent")

st.write("Enter your question about air quality data, and AI will generate an SQL query to fetch results.")

# User input field for SQL query
user_query = st.text_input("\U0001F50E Ask a question:", placeholder="Which location had the highest PM2.5 levels last year?")

# Submit button for SQL query
if st.button("Run Query"):
    if user_query:
        sql_query = generate_sql_query(user_query)
        st.write(f"\U0001F4CC **Generated SQL Query:**\n```sql\n{sql_query}\n```")

        results = ask_database(sql_query)

        if results:
            st.success("✅ Query executed successfully!")
            st.write("### Results:")
            st.table(results)
        else:
            st.warning("⚠️ No data found for this query.")
    else:
        st.error("⚠️ Please enter a question.")

# Trend Prediction Section
st.header("📈 Predict Future Air Quality Trends")

location_input = st.text_input("🌍 Enter a location:", placeholder="e.g., Los Angeles")

if st.button("Predict Trend"):
    if location_input:
        prediction = predict_air_quality_trend(location_input)
        st.write(prediction)
    else:
        st.error("⚠️ Please enter a location.")