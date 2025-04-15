# Suppress macOS warning
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

# --- Fix for importing settings module ---
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# ------------------------------------------

import cv2
import numpy as np
import json
import logging
import paho.mqtt.client as mqtt
from settings.settings import CAMERA, FACE_DETECTION, PATHS, MQTT
import base64

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# MQTT Configuration
MQTT_BROKER = MQTT['host']
MQTT_PORT = MQTT['port']
MQTT_TOPIC = MQTT['topic']

# Initialize MQTT Client
client = mqtt.Client()
try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()
    logger.info("Connected to MQTT broker")
except Exception as e:
    logger.error(f"Could not connect to MQTT broker: {e}")

def initialize_camera(camera_index: int = 0) -> cv2.VideoCapture:
    try:
        cam = cv2.VideoCapture(camera_index)
        if not cam.isOpened():
            logger.error("Could not open webcam")
            return None
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA['width'])
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA['height'])
        return cam
    except Exception as e:
        logger.error(f"Error initializing camera: {e}")
        return None

def load_names(filename: str) -> dict:
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as fs:
                content = fs.read().strip()
                if content:
                    return json.loads(content)
        return {}
    except Exception as e:
        logger.error(f"Error loading names: {e}")
        return {}

def start_face_recognition():
    try:
        logger.info("Starting face recognition system...")

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        if not os.path.exists(PATHS['trainer_file']):
            raise ValueError("Trainer file not found. Please train the model first.")
        recognizer.read(PATHS['trainer_file'])

        face_cascade = cv2.CascadeClassifier(PATHS['cascade_file'])
        if face_cascade.empty():
            raise ValueError("Error loading cascade classifier")

        cam = initialize_camera(CAMERA['index'])
        if cam is None:
            logger.warning("camera laaaaaa")
            raise ValueError("Failed to initialize camera")

        names = load_names(PATHS['names_file'])
        if not names:
            logger.warning("No names loaded, recognition will be limited")

        logger.info("Press 'CTRL + C' to exit.")

        while True:
            ret, img = cam.read()
            if not ret:
                logger.warning("Failed to grab frame")
                continue

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=FACE_DETECTION['scale_factor'],
                minNeighbors=FACE_DETECTION['min_neighbors'],
                minSize=FACE_DETECTION['min_size']
            )

            detected_name = None

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                id, confidence = recognizer.predict(gray[y:y+h, x:x+w])

                if confidence <= 100:
                    detected_name = names.get(str(id), "Unknown")
                    confidence_text = f"{confidence:.1f}%"

                    cv2.putText(img, detected_name, (x+5, y-5), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    cv2.putText(img, confidence_text, (x+5, y+h-5), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 1)

                    # Save detected face
                    face_img = img[y:y+h, x:x+w]
                    cv2.imwrite("face.jpg", face_img)

                    # Save result to JSON
                    with open("result.json", "w") as f:
                        json.dump({"name": detected_name}, f)

                    # Publish to MQTT
                    message = f"{detected_name} accepté !" if detected_name != "Unknown" else "Personne inconnue détectée !"
                    client.publish(MQTT_TOPIC, message)
                    logger.info(f"MQTT Message sent: {message}")

                    break  # Stop after first detected face

            if len(faces) > 0:
                break  # Stop main loop once a face is processed

        logger.info("Face recognition stopped")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

    finally:
        if 'cam' in locals() and cam:
            cam.release()
        client.loop_stop()
        cv2.destroyAllWindows()
