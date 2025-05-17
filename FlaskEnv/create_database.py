import sqlite3
from datetime import datetime

def create_database():
    try:
        # Connect to SQLite database (creates file if it doesn't exist)
        conn = sqlite3.connect("telemetry.db")
        cursor = conn.cursor()

        # Create telemetry_data table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS telemetry_data (
                time DATETIME,
                status TEXT,
                channel1 TEXT,
                channel2 TEXT,
                channel3 TEXT,
                channel4 TEXT,
                channel5 TEXT,
                channel6 TEXT,
                channel7 TEXT,
                channel8 TEXT
            )
        """)

        # Commit changes and close connection
        conn.commit()
        print("Database and table created successfully.")

    except sqlite3.Error as e:
        print(f"Error creating database: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    create_database()