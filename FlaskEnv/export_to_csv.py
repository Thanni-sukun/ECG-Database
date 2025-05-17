import sqlite3
import csv
from datetime import datetime

def export_to_csv():
    try:
        # Connect to SQLite database
        conn = sqlite3.connect("telemetry.db")
        cursor = conn.cursor()

        # Query all data from telemetry_data table
        cursor.execute("SELECT * FROM telemetry_data")
        rows = cursor.fetchall()

        # Define column headers
        columns = ["time", "status", "channel1", "channel2", "channel3", 
                   "channel4", "channel5", "channel6", "channel7", "channel8"]

        # Create CSV file and write data
        with open("telemetry_data.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            # Write header row
            writer.writerow(columns)
            # Write data rows
            writer.writerows(rows)

        print(f"Successfully exported {len(rows)} rows to telemetry_data.csv")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    export_to_csv()