import requests
import logging

logging.basicConfig(level=logging.INFO)

def fetch_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    logging.error("Failed to fetch data.")
    return None
