from flask import Flask, render_template, request, jsonify
import requests
import os
import json

app = Flask(__name__)

# Replace with your deployed model's Cloud Run URL
ML_MODEL_URL = "https://electricity-demand-forecasting-1010694068842.us-central1.run.app/predict"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Check if the post request has the file part
    if 'json_file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['json_file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Ensure it is a JSON file
    if file and file.filename.endswith('.json'):
        # Read the file content
        file_content = file.read().decode('utf-8')
        try:
            json_data = json.loads(file_content)

            # Send data to the machine learning model on Google Cloud Run
            response = requests.post(ML_MODEL_URL, json=json_data)

            # Handle the response from the model
            if response.status_code == 200:
                prediction = response.json()
                return jsonify(prediction)
            else:
                return jsonify({"error": "Prediction failed", "details": response.text}), response.status_code

        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON file"}), 400

    return jsonify({"error": "Invalid file format. Only JSON files are allowed."}), 400

# Run the Flask app. This will start the server, only for development only.  
if __name__ == '__main__':
    app.run(debug=True)
