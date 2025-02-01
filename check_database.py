import sqlite3

try:
    # Connect to SQLite database
    conn = sqlite3.connect("database/air_quality.sqlite")
    cursor = conn.cursor()

    # Get column names for the air_quality table
    cursor.execute("PRAGMA table_info(air_quality);")
    columns = cursor.fetchall()

    # Print column names
    print("Columns in air_quality table:", [col[1] for col in columns])

except Exception as e:
    print(f"Database error: {e}")

finally:
    conn.close()


