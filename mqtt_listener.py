import json
import os
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from handle_rfid import handle_uid
from ha import mqtt_publisher

load_dotenv()

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
SCANNER_ID = int(os.getenv("SCANNER_ID", "1"))
TOPIC = "token/dock/scan"


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected to MQTT broker, subscribing to {TOPIC}")
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload)
    except json.JSONDecodeError:
        print(f"Invalid JSON payload: {msg.payload}")
        return

    uid = data.get("uid")
    if not uid:
        print(f"Missing uid in payload: {data}")
        return

    scanner_id = data.get("scanner_id", SCANNER_ID)
    mac = data.get("mac")
    print(f"MQTT scan received: uid={uid} scanner={scanner_id} mac={mac}")
    result = handle_uid(uid, scanner_id=scanner_id, source="mqtt", mac=mac)
    mqtt_publisher.publish_result(scanner_id, result)


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
if MQTT_USERNAME:
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

print(f"Connecting to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}...")
client.connect(MQTT_BROKER, MQTT_PORT)
client.loop_forever()
