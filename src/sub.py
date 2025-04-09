import paho.mqtt.client as mqtt

# Configuration MQTT
BROKER = "localhost"  # Change this if needed
PORT = 1883
TOPIC = "jetbot/camera"

# Callback when the client receives a message
def on_message(client, userdata, message):
    print(message.payload.decode())  # Afficher seulement le contenu du message

# Create MQTT client
client = mqtt.Client()

# Set up callbacks
client.on_message = on_message

# Connect to the broker
client.connect(BROKER, PORT, 60)

# Subscribe to the topic
client.subscribe(TOPIC)

# Loop forever, waiting for messages
print(f"Subscribed to topic '{TOPIC}'... Waiting for messages.")
client.loop_forever()
