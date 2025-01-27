# Capstone Project - Air Pollution Data Agent

## Overview
This project provides a Streamlit-based user interface to fetch real-time air pollution data for any city using the OpenWeatherMap API. Users can enter a city name, and the app retrieves the Air Quality Index (AQI) and pollutant components.

## Features
- Retrieve and display AQI and pollutant components for any city.
- Dynamic city lookup using OpenWeatherMap Geocoding API.
- Displays pollutant levels in a table and interprets AQI with a user-friendly status (e.g., "Moderate").
- Logs all actions (e.g., API calls, errors) to the console.

## Requirements
- Python ≤ 3.12
- OpenWeatherMap API key (free to sign up)

## Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
