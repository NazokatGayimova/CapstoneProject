import sqlite3
import numpy as np
import pandas as pd
import requests
import openai
import os
import json
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


def ai_predict_air_quality_trend(location, historical_data):
    """Use OpenAI function calling to generate a customized air quality prediction."""
    trend_description = ""
    if historical_data:
        trend_description = f"Historical air quality data: {historical_data}. "
    else:
        trend_description = "No historical data is available for this city. Using global trends instead. "

    prompt = (f"Based on available data, predict the future air quality trend for {location}. "
              f"Consider pollution levels, environmental policies, and global trends. "
              f"{trend_description}")

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": "You are an AI trained to analyze and predict air quality trends."},
                      {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return "⚠️ AI function calling failed. Please check OpenAI API."


def predict_air_quality_trend(location):
    """Predict future air quality trend based on historical data or AI-based prediction."""
    data = get_historical_data(location)
    if data:
        years = np.array([row[0] for row in data]).reshape(-1, 1)
        pm_values = np.array([row[1] for row in data])
        if len(years) < 2:
            return ai_predict_air_quality_trend(location, historical_data=None)
        model = LinearRegression()
        model.fit(years, pm_values)
        next_year = np.array([[int(years[-1][0]) + 1]])
        predicted_pm = model.predict(next_year)[0]
        return f"📊 Predicted PM2.5 level for {location} in {next_year[0][0]}: **{predicted_pm:.2f} µg/m³**."
    else:
        return ai_predict_air_quality_trend(location, historical_data=None)


if __name__ == "__main__":
    location_input = input("Enter a location: ")
    prediction = predict_air_quality_trend(location_input)
    print(prediction)
