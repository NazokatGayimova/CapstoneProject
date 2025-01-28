🌍 Capstone Project: Air Pollution Data Agent
🎯 Overview
This project is a Streamlit-based app that provides real-time air pollution data for any city in the world. Users can:

Enter a city name to get air quality information.
See detailed pollutant levels, the Air Quality Index (AQI), and an interpretation of air quality (e.g., "Moderate").
Get interactive visuals for pollutant levels.
It’s simple, fast, and accessible—ideal for anyone who needs air quality insights at their fingertips!

🚀 Features
Real-Time Air Pollution Data: Fetch AQI and detailed pollutant levels from OpenWeatherMap's API.
Multi-City Support: Input any city name and get results instantly.
Data Visualization: Bar charts make it easy to compare pollutant levels.
Interactive UI: Built with Streamlit for simplicity and usability.
Logs for Developers: The app prints logs to the console for debugging and tracking API calls.
🛠️ Tools and Technologies
Streamlit: For creating the interactive user interface.
OpenWeatherMap API:
Geocoding API: Converts city names to latitude and longitude.
Air Pollution API: Provides AQI and pollutant data.
Python: The app is built entirely in Python.
Libraries Used:
requests for API calls.
pandas for data handling.
logging for debugging.
📋 Requirements
Before you start, ensure you have:

Python ≤ 3.12 installed.
An API key from OpenWeatherMap (free to sign up).
🖥️ Installation Instructions
Follow these steps to set up and run the app on your computer:

1️⃣ Clone the Repository
Download the project files to your computer:

bash
Copy
Edit
git clone https://github.com/NazokatGayimova/CapstoneProject.git
cd CapstoneProject
2️⃣ Set Up a Virtual Environment
Create and activate a virtual environment to keep dependencies organized:

macOS/Linux:
bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate
Windows:
bash
Copy
Edit
python -m venv venv
.\venv\Scripts\activate
3️⃣ Install Dependencies
Install all required libraries using pip:

bash
Copy
Edit
pip install -r requirements.txt
4️⃣ Add Your API Key
Open the app.py file in a text editor.
Find the line where the API key is defined:
python
Copy
Edit
API_KEY = "your_api_key_here"
Replace "your_api_key_here" with your OpenWeatherMap API key.
5️⃣ Run the App
Start the Streamlit app:

bash
Copy
Edit
streamlit run app.py
You’ll see a URL in the terminal (e.g., http://localhost:8501). Open this link in your browser to use the app.

📊 How to Use the App
Open the App: Follow the setup instructions to launch the app in your browser.
Enter a City Name: Type a city (e.g., "Tashkent" or "New York") into the input box and hit "Get Air Pollution Data."
View Results:
Air Quality Index (AQI): A single number representing the air quality.
Pollutant Levels: A table and bar chart showing detailed levels of pollutants like CO, PM2.5, and O3.
Air Quality Status: A description of the air quality (e.g., "Good," "Moderate," "Poor").
📜 Example Output
Input:
Shanghai

Output:
Air Quality Index (AQI): 3 (Moderate)

Pollutant Levels:

Pollutant	Value
CO	580.79
NO2	74.71
PM2.5	35.28
Visuals: A bar chart displaying pollutant levels.

Air Quality Status: "Moderate"

🐞 Logs and Debugging
The app prints logs to the terminal to help track:

Successful API calls.
Errors (e.g., invalid city names or API failures).
Example log:

ruby
Copy
Edit
INFO:root:Fetching coordinates for Tashkent...
INFO:root:Fetching air pollution data for lat=41.2995, lon=69.2401...
ERROR:root:City not found.
🌐 Deployment (Optional)
You can deploy this app online using Streamlit Cloud:

Push your project to GitHub.
Go to Streamlit Cloud and connect your GitHub repository.
Deploy your app and share the link with others.
🙋 FAQ
1. How do I get an OpenWeatherMap API key?
Sign up at OpenWeatherMap.
Go to your profile → API keys → Generate a new key.
2. What if the app doesn’t run?
Make sure all dependencies are installed:
bash
Copy
Edit
pip install -r requirements.txt
Ensure your API key is correctly added to app.py.
3. Can I use a different API?
Yes, you can extend the app by integrating other APIs for weather or notifications.
💡 Ideas for Future Enhancements
Add historical air quality trends.
Integrate weather data for a more comprehensive view.
Allow users to set notifications for poor air quality.
🤝 Contribution
Feel free to fork this repository, make improvements, and submit a pull request!

📞 Contact
For questions or collaboration, reach out at:

Email: nazokat_gayimova@epam.com
GitHub: NazokatGayimova