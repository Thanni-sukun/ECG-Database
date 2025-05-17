from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
import json

app = Flask(__name__)

def db_connection():
    try:
        conn = sqlite3.connect("telemetry.db")
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

@app.route("/telemetry", methods=["POST"])
def receive_telemetry():
    # Log the incoming request
    print(f"Received request: {request.method} {request.url}")
    print(f"Headers: {request.headers}")
    raw_data = request.get_data(as_text=True)
    print(f"Raw Body: {raw_data}")

    # Check if request contains JSON data
    if not request.is_json:
        print("Error: Request does not contain JSON data")
        return jsonify({"error": "Request must contain JSON data", "raw_body": raw_data}), 400

    # Attempt to parse JSON data
    try:
        data = request.get_json()
        print(f"Parsed JSON: {data}")
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON - {str(e)}")
        return jsonify({"error": f"Failed to parse JSON: {str(e)}", "raw_body": raw_data}), 400

    # Validate required fields
    required_fields = ["status", "channel1", "channel2", "channel3", "channel4", 
                       "channel5", "channel6", "channel7", "channel8"]
    if not all(field in data for field in required_fields):
        print("Error: Missing required fields")
        return jsonify({"error": "Missing required fields", "received_data": data}), 400

    # Get current timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Extract data
    status = data["status"].lstrip("\r")  # Remove leading \r if present
    channel1 = data["channel1"]
    channel2 = data["channel2"]
    channel3 = data["channel3"]
    channel4 = data["channel4"]
    channel5 = data["channel5"]
    channel6 = data["channel6"]
    channel7 = data["channel7"]
    channel8 = data["channel8"]

    # Store data in database
    conn = db_connection()
    if conn is None:
        print("Error: Database connection failed")
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO telemetry_data (time, status, channel1, channel2, channel3, 
                                       channel4, channel5, channel6, channel7, channel8)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (current_time, status, channel1, channel2, channel3, 
              channel4, channel5, channel6, channel7, channel8))
        conn.commit()
        print("Data stored successfully")
        return jsonify({"message": "Data stored successfully"}), 200

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return jsonify({"error": "Failed to store data"}), 500
    finally:
        if conn:
            conn.close()

@app.route("/telemetry", methods=["GET"])
def get_telemetry():
    print(f"Received request: {request.method} {request.url}")
    conn = db_connection()
    if conn is None:
        print("Error: Database connection failed")
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM telemetry_data")
        rows = cursor.fetchall()
        columns = ["time", "status", "channel1", "channel2", "channel3", 
                   "channel4", "channel5", "channel6", "channel7", "channel8"]
        data = [dict(zip(columns, row)) for row in rows]
        print(f"Retrieved {len(data)} rows from database")
        return jsonify(data), 200

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return jsonify({"error": "Failed to retrieve data"}), 500
    finally:
        if conn:
            conn.close()

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Telemetry Server is running"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)