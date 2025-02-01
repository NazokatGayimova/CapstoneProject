import sqlite3
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

DATABASE = "database/air_quality.sqlite"


def predict_air_quality_trend(location):
    """Predicts future air pollution trends using historical PM2.5 data."""
    conn = sqlite3.connect(DATABASE)

    # Get historical PM2.5 data
    query = f"""
    SELECT year, pm2_5 FROM air_quality 
    WHERE location = '{location}'
    ORDER BY year ASC;
    """

    data = pd.read_sql(query, conn)
    conn.close()

    if data.empty:
        return f"No data available for {location}."

    # Convert to NumPy arrays for regression
    years = np.array(data["year"], dtype=int).reshape(-1, 1)
    pm_values = np.array(data["pm2_5"])

    # Train Linear Regression model
    model = LinearRegression()
    model.fit(years, pm_values)

    next_year = np.array([[max(years) + 1]])
    predicted_pm = model.predict(next_year)[0]

    return f"📊 Predicted PM2.5 level for {location} in {int(next_year[0][0])}: {predicted_pm:.2f}"
