import os
import openai
import sqlite3
import re
from dotenv import load_dotenv
from tenacity import retry, wait_random_exponential, stop_after_attempt

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Ensure API key is set
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("\u274c OpenAI API key is missing! Check your .env file.")

MODEL = "gpt-3.5-turbo-0125"
DATABASE = "database/air_quality.sqlite"


@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, functions=None, model=MODEL):
    """Requests OpenAI ChatCompletion API."""
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=messages,
            functions=functions if functions else None
        )

        # Debugging: Print API response
        print("API Response:", response)

        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return None  # Return None instead of crashing


def generate_sql_query(user_query):
    """Converts a natural language question into an SQL query using OpenAI."""
    messages = [
        {"role": "system", "content": """You are an AI assistant that generates SQL queries for an air quality database. 
        The table name is `air_quality`. The correct column for locations is `location`. 
        The correct column for PM2.5 values is `pm2_5`. 
        The correct column for date filtering is `year`. 
        Instead of using dynamic date functions, always select the most recent available year using:
        `year = (SELECT MAX(year) FROM air_quality)`.
        Your response must only contain the SQL query, nothing else."""},
        {"role": "user", "content": user_query}
    ]

    response = chat_completion_request(messages)

    if response is None:
        return "Error generating SQL query: No response from OpenAI API."

    try:
        sql_query = response.choices[0].message.content

        # Extract SQL query from AI response (remove markdown formatting)
        match = re.search(r"```sql\n(.*?)\n```", sql_query, re.DOTALL)
        if match:
            sql_query = match.group(1).strip()  # Extract only the SQL part

        return sql_query
    except Exception as e:
        return f"Error generating SQL query: {e}"


def ask_database(query):
    """Executes an AI-generated SQL query on the SQLite database."""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return results  # Successfully return results
    except Exception as e:
        print(f"SQL Execution Error: {e}")  # Print SQL error message
        return None  # Return None if an error occurs
    finally:
        conn.close()  # Always close the database connection


if __name__ == "__main__":
    user_input = "Which location had the highest PM2.5 levels last year?"
    sql_query = generate_sql_query(user_input)
    print(f"Generated SQL Query: {sql_query}")

    results = ask_database(sql_query)
    print(f"Results: {results}")
