import requests
import logging
import streamlit as st

logging.basicConfig(level=logging.INFO)

API_KEY = "b8051d817b22bfb0aa796d0477465a59"  # Your API key

# Function to fetch air pollution data
def fetch_air_pollution_data(lat, lon, api_key):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['list'][0]
        else:
            logging.error(f"Failed to fetch air pollution data. Status code: {response.status_code}")
            return None
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None

# Function to fetch city coordinates
def get_city_coordinates(city_name, api_key):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200 and response.json():
            city_data = response.json()[0]
            return city_data["lat"], city_data["lon"]
        else:
            logging.error(f"Failed to fetch coordinates for {city_name}. Status code: {response.status_code}")
            return None, None
    except Exception as e:
        logging.error(f"An error occurred while fetching coordinates: {e}")
        return None, None

# Streamlit app
def main():
    st.title("Capstone Project UI")
    st.write("Welcome! Get real-time air pollution data for any city.")

    city = st.text_input("Enter a city:", "Tashkent")

    if st.button("Get Air Pollution Data"):
        lat, lon = get_city_coordinates(city, API_KEY)
        if lat and lon:
            data = fetch_air_pollution_data(lat, lon, API_KEY)
            if data:
                aqi = data['main']['aqi']
                st.metric("Air Quality Index (AQI)", aqi)

                # Display pollutant components
                components = data['components']
                st.write("Pollutant Components:")
                st.table(components)

                # AQI Interpretation
                aqi_interpretation = {
                    1: "Good",
                    2: "Fair",
                    3: "Moderate",
                    4: "Poor",
                    5: "Very Poor"
                }
                st.write(f"Air Quality Status: {aqi_interpretation.get(aqi, 'Unknown')}")
            else:
                st.error("Failed to fetch air pollution data.")
        else:
            st.error("Could not find the city. Please check the name and try again.")

if __name__ == "__main__":
    main()
