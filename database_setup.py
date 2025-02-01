import sqlite3
import pandas as pd
import re

# Load dataset
file_path = "data/Air_Quality.csv"
df = pd.read_csv(file_path)

# Rename columns for SQLite compatibility
df = df.rename(columns={"Geo Place Name": "location", "Data Value": "pm2_5", "Start_Date": "date", "Time Period": "time_period"})

# Convert date format for SQLite
df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.strftime("%Y-%m-%d")

# Ensure 'pm2_5' is stored as a float (REAL)
df["pm2_5"] = pd.to_numeric(df["pm2_5"], errors="coerce")

# Extract first 4-digit year from "Time Period"
def extract_year(value):
    match = re.search(r'(\d{4})', str(value))  # Extract first 4-digit number
    return match.group(1) if match else None

df["year"] = df["time_period"].astype(str).apply(extract_year)

# Drop rows with missing values in critical columns
df = df.dropna(subset=["location", "pm2_5", "date", "year"])

# Connect to SQLite
conn = sqlite3.connect("database/air_quality.sqlite")
cursor = conn.cursor()

# Create table (overwrite the old one)
cursor.execute("""
DROP TABLE IF EXISTS air_quality;
""")

cursor.execute("""
CREATE TABLE air_quality (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location TEXT,
    date TEXT,
    time_period TEXT,
    year TEXT,
    pm2_5 REAL
);
""")

# Insert data into table
df.to_sql("air_quality", conn, if_exists="replace", index=False)

print("✅ Database setup complete!")
conn.close()
