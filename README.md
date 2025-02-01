📌 README.md (Final & Detailed Version)
markdown
Copy
Edit
# 🌍 AI-Powered Air Quality Query Agent

## 🚀 Overview
This project is an **AI-powered air quality query agent** that allows users to:
1. **Query historical air quality data** using an SQL-based database.
2. **Predict future air quality trends** for a given location.
3. **Guide users to OpenWeather if no data is available** in the database.

It uses:
- **OpenAI GPT** to generate SQL queries dynamically.
- **SQLite** as a local database for storing air quality data.
- **Streamlit** for an interactive and user-friendly web interface.
- **Scikit-learn** for predictive modeling of air quality trends.

---

## 📂 **Project Structure**
📦 CapstoneProject_AI │── 📁 database │ ├── air_quality.sqlite # SQLite database containing air quality data │── 📁 data │ ├── Air_Quality.csv # Raw dataset from Kaggle │── 📄 app.py # Streamlit-based web interface │── 📄 ai_query_agent.py # AI-powered SQL query agent │── 📄 predict_trend.py # Air quality prediction model │── 📄 database_setup.py # Script to initialize the SQLite database │── 📄 requirements.txt # Python dependencies │── 📄 README.md # Project documentation

yaml
Copy
Edit

---

## 🔧 **Installation & Setup**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/NazokatGayimova/CapstoneProject.git
cd CapstoneProject_AI
2️⃣ Set Up a Virtual Environment
bash
Copy
Edit
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
(For Windows: .\venv\Scripts\activate)

3️⃣ Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4️⃣ Set Up Environment Variables
Create a .env file in the project root:

ini
Copy
Edit
OPENAI_API_KEY=your_openai_api_key_here
🏃 Running the Project
Start the Streamlit App
bash
Copy
Edit
streamlit run app.py
It will be accessible at:
➡️ http://localhost:8501/

🛠️ How It Works
1️⃣ AI-Powered SQL Querying
Users enter air quality-related questions (e.g., "What is the air quality in New York?").
AI converts this into an SQL query.
The system searches the database and returns relevant results.
If no data is found, users are guided to OpenWeather.
2️⃣ Air Quality Trend Prediction
Users enter a location for future air quality predictions.
The system uses historical data and machine learning (Linear Regression) to predict PM2.5 levels.
🔍 Example Queries
✅ "What is the air quality in London?"
✅ "Show air pollution levels for Tokyo."
✅ "Find the latest PM2.5 levels in Paris."

If data is unavailable, the system displays:
⚠️ "No data found. Please visit OpenWeather for more information."

🤝 Contributing
Fork the repository.
Create a new branch (feature-xyz).
Make changes & commit (git commit -m "Added feature XYZ").
Push & submit a PR (git push origin feature-xyz).
🛠 Troubleshooting
1️⃣ Database Not Found?
Run the database setup script:

bash
Copy
Edit
python database_setup.py
2️⃣ Errors with OpenAI API?
Ensure you have a valid API key set in .env.
Run:
bash
Copy
Edit
pip install --upgrade openai
📜 License
This project is open-source under the MIT License.

🎯 Future Enhancements
✅ Add real-time API integration for live air quality updates.
✅ Improve AI query handling to reduce errors.
✅ Implement more advanced machine learning models for predictions.
