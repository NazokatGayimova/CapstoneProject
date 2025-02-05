# 🌍 AI-Powered Air Quality Query Agent

## 🚀 Overview
This project is an **AI-powered air quality query agent** that allows users to:
1. **Query historical air quality data** using an SQL-based database.
2. **Predict future air quality trends** using AI and machine learning.
3. **Retrieve real-time air quality data** from OpenWeather API.
4. **Fetch AI-generated insights** from web sources if data is unavailable.
5. **Utilize OpenAI function calling** to make intelligent decisions dynamically.

It uses:
- **OpenAI GPT-4 Turbo** for function calling, query generation, and trend analysis.
- **SQLite** for storing historical air quality data.
- **Streamlit** for an interactive web interface.
- **Scikit-learn** for predictive modeling of air quality trends.
- **OpenWeather API** for real-time pollution levels.

---

## 📂 **Project Structure**
```
📦 CapstoneProject_AI
│── 📁 database
│   ├── air_quality.sqlite  # SQLite database containing air quality data
│── 📁 data
│   ├── Air_Quality.csv  # Raw dataset from Kaggle
│── 📄 app.py  # Streamlit-based web interface
│── 📄 ai_query_agent.py  # AI-powered SQL query & API fetcher
│── 📄 predict_trend.py  # AI-powered air quality prediction model
│── 📄 database_setup.py  # Script to initialize the SQLite database
│── 📄 requirements.txt  # Python dependencies
│── 📄 README.md  # Project documentation
```

---

## 🔧 **Installation & Setup**

### **1️⃣ Clone the Repository**
```bash
git clone <your-github-repo-url>
cd CapstoneProject_AI
```

### **2️⃣ Set Up a Virtual Environment**
```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# For Windows: .venv\Scripts\activate
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Set Up API Keys**
Create a `.env` file in the project root:
```ini
OPENAI_API_KEY=your_openai_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
```

---

## 🏃 Running the Project
### **Start the Streamlit App**
```bash
streamlit run app.py
```
It will be accessible at:
➡️ `http://localhost:8501/`

---

## 🛡️ Security Enhancements
To improve security, we have implemented the following updates:
- **🔒 Secure API Key Management:** API keys are now stored in a `.env` file instead of hardcoded in the script.
- **🛠️ SQL Injection Prevention:** All database queries use **parameterized queries** to prevent SQL injection attacks.
- **🚫 API Error Handling:** OpenAI and OpenWeather API calls now include structured error handling to avoid crashes.
- **🔑 Data Privacy:** User inputs are validated to prevent malicious requests and unnecessary API calls.
- **🛡️ Exception Handling:** Enhanced error handling ensures robustness in unexpected scenarios.

---

## 🛠️ How It Works

### **1️⃣ AI-Powered SQL Querying**
- Users enter air quality-related questions (e.g., _"What is the air quality in New York?"_).
- AI converts this into an SQL query.
- The system searches the database and returns relevant results.
- If no data is found, users are guided to OpenWeather or AI-generated insights.

### **2️⃣ AI-Powered Air Quality Trend Prediction**
- Users enter a location for **future air quality predictions**.
- The system uses **historical data** and **machine learning** (Linear Regression) to predict PM2.5 levels.
- If no historical data exists, **AI generates a location-specific forecast** based on environmental factors.

### **3️⃣ Real-Time Air Quality Retrieval**
- If no historical data is available, the system fetches **real-time pollution levels** from OpenWeather API.
- Data is formatted in **human-readable output** (AQI interpretation, pollutant levels in µg/m³).
- If OpenWeather API fails, AI searches the web for **trusted sources** (WHO, AQICN, EPA).

### **4️⃣ OpenAI Function Calling Integration**
- The AI system **automatically determines** the best course of action:
  - Query database for historical data.
  - Fetch real-time air quality.
  - Use AI to predict future trends.
- **No manual decision-making required—AI handles everything dynamically.**

---

## 🔍 Example Queries
✅ _"What is the air quality in London?"_
✅ _"Show air pollution levels for Tokyo."_
✅ _"Find the latest PM2.5 levels in Paris."_
✅ _"Predict the air quality trend for Beijing."_
✅ _"What will be the pollution levels in Tokyo next year?"_

If data is unavailable, the system now displays:
⚠️ _"No real-time air quality data available for [city]. Please check OpenWeather."_

---

## 🛠 Troubleshooting
### **1️⃣ Database Not Found?**
Run the database setup script:
```bash
python database_setup.py
```

### **2️⃣ Errors with OpenAI or OpenWeather API?**
Ensure you have a valid API key set in `.env`.
Then run:
```bash
pip install --upgrade openai
```

---

## 📜 License
This project is open-source under the **MIT License**.

---

## 🎯 Future Enhancements
✅ **Integrate real-time API for live air quality updates**
✅ **Improve AI query handling for location-based searches**
✅ **Enhance ML models for better prediction accuracy**
✅ **Optimize caching for external API calls**
