from flask import Flask, request, jsonify

app = Flask(__name__)

# Expected headers
EXPECTED_AUTH = "Sentinel/Anticheat"
EXPECTED_SPECIAL_KEY = "___CELESTIAL_CLIENT_KEY.DO_NOT_SHARE_OR_SCREENSHARE_THIS.FDSAFJ129JI31029I312931J2931J2391J0231902J31902J3192J"

# File to store the data
DATA_FILE = "received_data.txt"

@app.route('/requests', methods=['POST'])
def handle_request():
    # Get headers from the request
    auth_header = request.headers.get('Authorization')
    special_key_header = request.headers.get('Special Key')

    # Validate headers
    if auth_header != EXPECTED_AUTH or special_key_header != EXPECTED_SPECIAL_KEY:
        return jsonify({"error": "Unauthorized: Invalid headers"}), 401

    # Get JSON data from the request body
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Format the data as "data data data"
    formatted_data = " ".join(str(value) for value in data.values())

    # Append the formatted data to the file
    with open(DATA_FILE, "a") as file:
        file.write(formatted_data + "\n")

    # Respond with success
    return jsonify({"message": "Request received", "data": data}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
