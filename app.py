from flask import Flask, request, jsonify
import subprocess
import threading

app = Flask(__name__)

def run_recognizer():
    try:
        subprocess.run(["python3", "face_recognizer.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running face_recognizer.py: {e}")

def run_register():
    try:
        subprocess.run(["python3", "face_taker.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running face_taker.py: {e}")

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
    app.run(host='0.0.0.0', port=5000, debug=True)
