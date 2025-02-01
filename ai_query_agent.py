import sqlite3
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# Function to retrieve database schema
def get_database_schema():
    """Retrieve database schema dynamically."""
    conn = sqlite3.connect("database/air_quality.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    schema_info = {}
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [col[1] for col in cursor.fetchall()]
        schema_info[table_name] = columns

    conn.close()
    return schema_info


# Function to generate SQL query using OpenAI
def generate_sql_query(user_query):
    """Generate an SQL query based on user input and database schema."""
    schema_info = get_database_schema()
    prompt = f"""
    You are an SQL assistant with access to the following database schema:
    {schema_info}
    Given this schema, generate an appropriate SQL query for the user's request:
    "{user_query}"
    Ensure the SQL is correctly formatted and avoids non-existing table or column names.
    Do not include explanations, only return the SQL query.
    """
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are an expert SQL assistant."},
                      {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating SQL query: {e}"


# Function to query the database
def ask_database(query):
    """Execute SQL query and return results."""
    try:
        conn = sqlite3.connect("database/air_quality.sqlite")
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return rows if rows else "Please visit openweather.com for more information."
    except Exception as e:
        return f"SQL error: {e}"


# Main function to handle user queries
def handle_query(user_query):
    """Process user query and return results from database or OpenWeather prompt."""
    sql_query = generate_sql_query(user_query)
    if "Error" in sql_query:
        return "Please visit openweather.com for more information."

    return ask_database(sql_query)


if __name__ == "__main__":
    user_input = input("Enter your air quality question: ")
    response = handle_query(user_input)
    print(response)
