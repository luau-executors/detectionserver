from flask import Flask, request, jsonify, send_file
import os

app = Flask(__name__)

# Expected headers
EXPECTED_AUTH = "Sentinel/Anticheat"
EXPECTED_SPECIAL_KEY = "Celestial/ClientKey3014"

# File paths
DATA_FILE = "received_data.txt"
LOG_FILE = "request_log.txt"

# Ensure the files exist and initialize them
for file in [DATA_FILE, LOG_FILE]:
    with open(file, "w") as f:
        f.write("# Log initialized\n")

@app.route('/requests', methods=['POST'])
def handle_request():
    # Get headers from the request
    auth_header = request.headers.get('Authorization')
    special_key_header = request.headers.get('SpecialKey')

    # Validate headers
    if auth_header != EXPECTED_AUTH or special_key_header != EXPECTED_SPECIAL_KEY:
        return jsonify({"error": "Unauthorized: Invalid headers"}), 401

    # Get JSON data from the request body
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Format the data as "data data data"
    formatted_data = " ".join(str(value) for value in data.values())

    # Append the formatted data to the received data file
    with open(DATA_FILE, "a") as file:
        file.write(formatted_data + "\n")
    
    # Log the request details
    with open(LOG_FILE, "a") as log:
        log.write(f"Received request: {data}\n")

    # Respond with success
    return jsonify({"message": "Request received", "data": data}), 200

@app.route('/received_data.txt', methods=['GET'])
def get_data_file():
    return send_file(DATA_FILE, mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
