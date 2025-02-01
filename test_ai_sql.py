import sqlite3

try:
    # Connect to SQLite database
    conn = sqlite3.connect("database/air_quality.sqlite")
    cursor = conn.cursor()

    # Corrected query with 'Time Period' instead of 'time_period'
    query = """
    SELECT location
    FROM air_quality
    WHERE "Time Period" = strftime('%Y', date('now', '-1 year'))
    ORDER BY pm2_5 DESC
    LIMIT 1;
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    print("Query Results:", rows)

except Exception as e:
    print(f"SQL Execution Error: {e}")

finally:
    conn.close()
