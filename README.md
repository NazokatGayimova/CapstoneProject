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
    
    formatted_data = {
        "location": location,
        "aqi": aqi,
        "pollutants": {
            "CO (Carbon Monoxide)": f"{components['co']} µg/m³",
            "NO (Nitric Oxide)": f"{components['no']} µg/m³",
            "NO₂ (Nitrogen Dioxide)": f"{components['no2']} µg/m³",
            "O₃ (Ozone)": f"{components['o3']} µg/m³",
            "SO₂ (Sulfur Dioxide)": f"{components['so2']} µg/m³",
            "PM2.5 (Fine Particles)": f"{components['pm2_5']} µg/m³",
            "PM10 (Coarse Particles)": f"{components['pm10']} µg/m³",
            "NH₃ (Ammonia)": f"{components['nh3']} µg/m³",
        }
    }
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
    """Process user query with OpenAI function calling."""
    function_definitions = [
        {
            "name": "fetch_air_quality",
            "description": "Fetch real-time air quality for a location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "City name"}
                },
                "required": ["location"]
            }
        }
    ]
    
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": "You are an AI assistant that calls functions."},
                      {"role": "user", "content": user_query}],
            functions=function_definitions,
            function_call="auto"
        )
        
        function_response = response.choices[0].message.function_call
        if function_response and function_response.name == "fetch_air_quality":
            args = json.loads(function_response.arguments)
            return fetch_external_air_quality(args.get("location"))
        else:
            return "⚠️ Unable to process request."
    except Exception:
        return "⚠️ AI function calling failed. Please check OpenAI API."

