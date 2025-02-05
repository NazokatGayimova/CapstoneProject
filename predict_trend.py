import sqlite3
import numpy as np
import pandas as pd
import requests
import openai
import os
from sklearn.linear_model import LinearRegression
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Initialize OpenAI Client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def get_historical_data(location):
    """Retrieve historical air quality data for the given location."""
    conn = sqlite3.connect("database/air_quality.sqlite")
    cursor = conn.cursor()

    cursor.execute("SELECT year, pm2_5 FROM air_quality WHERE location = ? ORDER BY year", (location,))
    data = cursor.fetchall()
    conn.close()

    return data if data else None

def fetch_real_time_air_quality(location):
    """Fetch real-time air quality data from OpenWeather API."""
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?q={location}&appid={OPENWEATHER_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if "list" in data and len(data["list"]) > 0:
            return data["list"][0]["components"]
        else:
            return None
    except requests.exceptions.RequestException:
        return None

def ai_predict_air_quality_trend(location):
    """Use AI to predict air quality trends for locations with no historical data."""
    prompt = f"Predict the future air quality trend for {location} based on global pollution trends and regional factors. Provide a concise, data-driven forecast."
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": "You are an expert in air quality forecasting."},
                      {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return "⚠️ AI prediction failed. Please check reputable sources like WHO or AQICN."

def predict_air_quality_trend(location):
    """Predict future air quality trend based on historical data or AI-based prediction."""
    data = get_historical_data(location)
    if data:
        years = np.array([row[0] for row in data]).reshape(-1, 1)
        pm_values = np.array([row[1] for row in data])
        if len(years) < 2:
            return "⚠️ Insufficient data to predict air quality trends."
        model = LinearRegression()
        model.fit(years, pm_values)
        next_year = np.array([[int(years[-1][0]) + 1]])
        predicted_pm = model.predict(next_year)[0]
        return f"📊 Predicted PM2.5 level for {location} in {next_year[0][0]}: **{predicted_pm:.2f} µg/m³**."
    else:
        real_time_data = fetch_real_time_air_quality(location)
        if real_time_data:
            return f"🌍 Real-time air quality for {location}: {real_time_data}"
        else:
            return ai_predict_air_quality_trend(location)

if __name__ == "__main__":
    location_input = input("Enter a location: ")
    prediction = predict_air_quality_trend(location_input)
    print(prediction)
