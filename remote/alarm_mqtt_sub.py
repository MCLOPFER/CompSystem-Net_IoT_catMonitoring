#!/usr/bin/python3

import paho.mqtt.client as mqtt
from urllib.parse import urlparse
from requests import get
from alarm_api import start_backround_user_alarm_api
import json

# MQTT URL and topic configuration
URL = urlparse("mqtt://test:test@p51eac75.ala.dedicated.aws.emqxcloud.com:1883/p51eac75/home")
BASE_TOPIC = URL.path[1:]

# Event callback definitions
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        client.subscribe(f"{BASE_TOPIC}/#", qos=1)  # Subscribe to all subtopics
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, msg):
    print(f"Received message on topic '{msg.topic}': {msg.payload.decode()}")
    # If the motion topic recieves a message
    if msg.topic == f"{BASE_TOPIC}/motion":
        print("INFO: mation topic message recieved")
        # format the json to use double quotes
        msg_string = msg.payload.decode().replace("\'", "\"")
        # Load the json into a string
        msg_content = json.loads(msg_string)
        # If the event value in the message is "motion detected"
        if msg_content["event"] == "motion_detected":
            print("INFO: recieved motion detected event")
            # use a GET request to trigger alarm via API on the local host
            get("http://127.0.0.1:5000/trigger_user_alarm")

def on_subscribe(client, userdata, mid, granted_qos):
    print(f"Subscribed with QoS {granted_qos[0]}")

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT broker")
    if rc != 0:
        print("Unexpected disconnection. Attempting to reconnect...")
        try:
            client.reconnect()
        except Exception as e:
            print(f"Reconnection failed: {e}")


mqttc = mqtt.Client()
# Assign callbacks
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe
mqttc.on_disconnect = on_disconnect

# Set username and password if provided in the URL
if URL.username:
    mqttc.username_pw_set(URL.username, URL.password)

# Start user alarm API process in the background
start_backround_user_alarm_api()

# Connect to the MQTT broker
mqttc.connect(URL.hostname, URL.port)
mqttc.loop_forever()