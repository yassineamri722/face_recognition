import requests
import base64
import cv2
import numpy as np

# URL de base
BASE_URL = "http://127.0.0.1:5000"

def safe_print_response(label, res):
    try:
        data = res.json()
        print(f"{label}: {res.status_code}", {"name": data.get("name")})

        # Show image if it exists
        if "image" in data and data["image"]:
            img_base64 = data["image"]
            img_bytes = base64.b64decode(img_base64)
            nparr = np.frombuffer(img_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if img is not None:
                cv2.imshow("Recognized Face", img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            else:
                print("Error decoding image")
        else:
            print("No image in response.")

    except Exception as e:
        print(f"{label}: {res.status_code} - Error parsing response:", e)
        print("Raw response:", res.text)

def test_index():
    try:
        res = requests.get(f"{BASE_URL}/")
        safe_print_response("Index", res)
    except requests.exceptions.RequestException as e:
        print("Index: Error -", e)

def test_recognize():
    try:
        res = requests.post(f"{BASE_URL}/recognize")
        safe_print_response("Recognize", res)
    except requests.exceptions.RequestException as e:
        print("Recognize: Error -", e)

def test_register():
    try:
        payload = {
            "username": "test_user",
            "email": "test@example.com"
        }
        res = requests.post(f"{BASE_URL}/register", json=payload)
        safe_print_response("Register", res)
    except requests.exceptions.RequestException as e:
        print("Register: Error -", e)

if __name__ == "__main__":
    test_recognize()
