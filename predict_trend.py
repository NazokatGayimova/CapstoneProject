import openai
import os
import sqlite3
import pandas as pd
from dotenv import load_dotenv

# Load API key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Ensure API key is set
if not OPENAI_API_KEY:
    raise ValueError("\u274c OpenAI API key is missing! Check your .env file.")

client = openai.OpenAI(api_key=OPENAI_API_KEY)


def predict_air_quality_trend(location):
    """Predicts future air quality trends based on historical data or AI assistance"""
    try:
        conn = sqlite3.connect("database/air_quality.sqlite")
        query = f"""
        SELECT year, pm2_5 FROM air_quality 
        WHERE location = '{location}' 
        ORDER BY year ASC;
        """
        df = pd.read_sql(query, conn)
        conn.close()

        if df.empty:
            # If no data is found, use AI assistance
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"Predict future air quality for {location}."}]
            )
            return response.choices[0].message.content.strip()

        # Implement a simple prediction model using linear regression
        from sklearn.linear_model import LinearRegression
        import numpy as np

        df = df.dropna()
        if df.empty:
            return "⚠️ No valid historical data available for prediction."

        X = df['year'].values.reshape(-1, 1)
        y = df['pm2_5'].values

        model = LinearRegression()
        model.fit(X, y)
        next_year = np.array([[max(df['year']) + 1]])
        predicted_pm = model.predict(next_year)[0]

        return f"Predicted PM2.5 level for {next_year[0][0]}: {predicted_pm:.2f}"
    except Exception as e:
        return f"❌ Prediction error: {str(e)}"
