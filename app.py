from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS
import os
import json
import base64

# Import your function
from src.face_recognizer import start_face_recognition

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/recognize', methods=['POST'])
def recognize():
    # Clean old files
    for f in ['result.json', 'face.jpg']:
        if os.path.exists(f):
            os.remove(f)

    # Run face recognition
    start_face_recognition()

    # Prepare the result dictionary
    result = {"name": None, "image": None}

    # Load result.json if exists
    if os.path.exists("result.json"):
        with open("result.json", "r") as f:
            result.update(json.load(f))

    # Load and encode image if exists
    if os.path.exists("face.jpg"):
        with open("face.jpg", "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            result["image"] = encoded_image

    # Emit via WebSocket
    socketio.emit('face_recognized', result)

    return jsonify(result)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
