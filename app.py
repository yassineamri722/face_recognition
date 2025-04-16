from flask import Flask, jsonify
import os
import json
import base64

# Import the function from src
from src.face_recognizer import start_face_recognition

app = Flask(__name__)

@app.route('/recognize', methods=['POST'])
def recognize():
    # Remove previous files if they exist
    for f in ['result.json', 'face.jpg']:
        if os.path.exists(f):
            os.remove(f)

    # Call the face recognition function
    start_face_recognition()

    # Prepare the result dictionary
    result = {"name": None, "image": None}

    # Read the result if it exists
    if os.path.exists("result.json"):
        with open("result.json", "r") as f:
            result.update(json.load(f))

    # Read and encode the image if it exists
    if os.path.exists("face.jpg"):
        with open("face.jpg", "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            result["image"] = encoded_image

    return jsonify(result)

if __name__ == "__main__":
    # Run the app with gunicorn for production
    # For local development, use: app.run(host="0.0.0.0", port=5000, debug=True)
    app.run(host="0.0.0.0", port=5000, debug=False)
