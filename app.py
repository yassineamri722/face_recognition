from flask import Flask, request, jsonify
import subprocess
import threading

app = Flask(__name__)

def run_recognizer():
    subprocess.run(["python3", "face_recognizer.py"])

def run_register():
    subprocess.run(["python3", "face_taker.py"])

@app.route('/')
def index():
    return "Face Recognition Flask API is running!"

@app.route('/recognize', methods=['POST'])
def recognize():
    thread = threading.Thread(target=run_recognizer)
    thread.start()
    return jsonify({"status": "started", "message": "Face recognition started"}), 202

@app.route('/register', methods=['POST'])
def register():
    thread = threading.Thread(target=run_register)
    thread.start()
    return jsonify({"status": "started", "message": "Face capture started"}), 202

if __name__ == '__main__':
    app.run(debug=True)
