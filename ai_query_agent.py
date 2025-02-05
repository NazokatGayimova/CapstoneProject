import sqlite3
import openai
import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Initialize OpenAI Client
client = openai.OpenAI(api_key=OPENAI_API_KEY)


def get_location_coordinates(location):
    """Fetch latitude and longitude for a given location using OpenWeather Geocoding API."""
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={OPENWEATHER_API_KEY}"
    try:
        response = requests.get(geo_url)
        response.raise_for_status()
        data = response.json()
        if data and len(data) > 0:
            return data[0]['lat'], data[0]['lon']
        else:
            return None, None
    except requests.exceptions.RequestException:
        return None, None


def interpret_air_quality(aqi):
    """Convert AQI index to human-readable format."""
    aqi_levels = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}
    return aqi_levels.get(aqi, "Unknown")


def format_air_quality_data(data, location):
    """Convert raw API air quality data into human-readable format."""
    if not data:
        return f"⚠️ No real-time air quality data available for {location}."

    aqi = interpret_air_quality(data['main']['aqi'])
    components = data['components']

    formatted_data = (f"🌍 **Real-time Air Quality in {location}:**\n"
                      f"- **Overall Air Quality Index (AQI):** {aqi}\n"
                      f"- **CO (Carbon Monoxide):** {components['co']} µg/m³\n"
                      f"- **NO (Nitric Oxide):** {components['no']} µg/m³\n"
                      f"- **NO₂ (Nitrogen Dioxide):** {components['no2']} µg/m³\n"
                      f"- **O₃ (Ozone):** {components['o3']} µg/m³\n"
                      f"- **SO₂ (Sulfur Dioxide):** {components['so2']} µg/m³\n"
                      f"- **PM2.5 (Fine Particles):** {components['pm2_5']} µg/m³\n"
                      f"- **PM10 (Coarse Particles):** {components['pm10']} µg/m³\n"
                      f"- **NH₃ (Ammonia):** {components['nh3']} µg/m³")
    return formatted_data


def fetch_external_air_quality(location):
    """Fetch and format real-time air quality data using OpenWeather API."""
    lat, lon = get_location_coordinates(location)
    if lat is None or lon is None:
        return None  # No valid coordinates found

    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if "list" in data and len(data["list"]) > 0:
            return format_air_quality_data(data["list"][0], location)
        else:
            return None
    except requests.exceptions.RequestException:
        return None


def handle_query(user_query):
    """Process user query, decide action, and return results."""
    decision_prompt = f"""
    Given the user query: "{user_query}", decide the action:
    - If the query is about historical air quality, return "sql_query".
    - If the query is about predicting future trends, return "predict_trend".
    - If the query cannot be answered with the available data, return "fetch_external".
    Respond with one of these three choices only.
    """

    try:
        decision_response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": "Decide the appropriate action."},
                      {"role": "user", "content": decision_prompt}]
        )
        decision = decision_response.choices[0].message.content.strip()
    except Exception:
        return "⚠️ Unable to determine the correct action."

    if decision == "fetch_external":
        location = user_query.split()[-1]  # Extract last word as location
        external_data = fetch_external_air_quality(location)
        return external_data if external_data else f"⚠️ No real-time air quality data available for {location}. Please check OpenWeather."
    else:
        return "⚠️ Unexpected decision outcome."
