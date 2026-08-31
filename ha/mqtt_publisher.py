import json
import os

import paho.mqtt.publish as publish
from dotenv import load_dotenv

load_dotenv()

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
ACTION_TOPIC = "token/dock/action"
RESULT_TOPIC_PREFIX = "token/dock/result"
UNREGISTERED_UID_TOPIC = "token/dock/unregistered"


def publish_unregistered_uid(uid, scanner_id, mac=None):
    data = {"uid": uid, "scanner_id": scanner_id}
    if mac is not None:
        data["mac"] = mac
    payload = json.dumps(data)
    auth = (
        {"username": MQTT_USERNAME, "password": MQTT_PASSWORD}
        if MQTT_USERNAME
        else None
    )
    publish.single(
        UNREGISTERED_UID_TOPIC,
        payload=payload,
        hostname=MQTT_BROKER,
        port=MQTT_PORT,
        auth=auth,
    )
    print(f"MQTT published to {UNREGISTERED_UID_TOPIC}: {payload}")


def publish_action(uid, scanner_id, action, mac=None):
    data = {"uid": uid, "scanner_id": scanner_id, "action": action}
    if mac is not None:
        data["mac"] = mac
    payload = json.dumps(data)
    auth = (
        {"username": MQTT_USERNAME, "password": MQTT_PASSWORD}
        if MQTT_USERNAME
        else None
    )
    publish.single(
        ACTION_TOPIC, payload=payload, hostname=MQTT_BROKER, port=MQTT_PORT, auth=auth
    )
    print(f"MQTT published to {ACTION_TOPIC}: {payload}")


def publish_result(scanner_id, result):
    topic = f"{RESULT_TOPIC_PREFIX}/{scanner_id}"
    data = {"scanner_id": scanner_id, **result}
    payload = json.dumps(data)
    auth = (
        {"username": MQTT_USERNAME, "password": MQTT_PASSWORD}
        if MQTT_USERNAME
        else None
    )
    publish.single(
        topic, payload=payload, hostname=MQTT_BROKER, port=MQTT_PORT, auth=auth
    )
    print(f"MQTT published to {topic}: {payload}")
