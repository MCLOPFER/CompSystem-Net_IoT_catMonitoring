#!/usr/bin/python3

import paho.mqtt.client as mqtt
from urllib.parse import urlparse
from requests import post
from time import sleep
from gpiozero import MotionSensor


# parse mqtt url for connection details.
URL = urlparse("mqtt://test:test@p51eac75.ala.dedicated.aws.emqxcloud.com:1883/p51eac75/home")
BASE_TOPIC = URL.path[1:]
DEVICE_ID = "monitor"

# MQTT event callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
    else:
        print(f"Connection failed with code {rc}")

def on_publish(client, userdata, mid):
    print(f"Message ID: {mid} published successfully")

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT broker")
    if rc != 0:
        print("Unexpected disconnection. Reconnecting...")
        client.reconnect()

mqttc = mqtt.Client()

# Assign event callbacks
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish


# check if username and password in the url (there isn't in this basic example)
if (URL.username):
    mqttc.username_pw_set(URL.username, URL.password)
# Connect
mqttc.connect(URL.hostname, URL.port)
mqttc.loop_start()

def motion_detect():
    pir = MotionSensor(4)

    # Create a dictionary
    msgFromClient = {
        "deviceID": DEVICE_ID,
        "event": "motion_detected"
    }
    while True:
        print("INFO: waiting for motion")
        pir.wait_for_motion()
        print("INFO: motion detected")

        print("INFO: taking before pictures")
        picture_api_endpoint = "http://127.0.0.1:5000/camera/picture"
        # Take 2 before pictures 1 second apart
        for i in range(2):
            # JSON parameter list
            picture_params_json = {'deviceID': f'{DEVICE_ID}', 'image_name': f'before_monitor_image_{i}.jpg'}
            # POST request to take a picture
            picture_request = post(picture_api_endpoint, json = picture_params_json)
            print(f"INFO: RESPONSE: {picture_request}")
            sleep(1)
        
        # JSON parameter list for video
        video_params_json = {'deviceID': f'{DEVICE_ID}', 'duration': 5, 'video_name': 'before_monitor_video.mp4'}
        video_api_endpoint = "http://127.0.0.1:5000/camera/record"
        print("INFO: taking before video")
        # POST request to take the video
        post(video_api_endpoint, json = video_params_json)
        # Trigger alarm by publishing a message in the motion topic
        mqttc.publish(f"{BASE_TOPIC}/motion",str(msgFromClient))
        
        # wait 5 seconds for the alarm to scare off kittens
        sleep(5)
        
        print("INFO: taking after pictures")
        # Take 2 after pictures 1 second apart
        for i in range(2):
            # JSON parameter list
            picture_params_json = {'deviceID': f'{DEVICE_ID}', 'image_name': f'after_monitor_image_{i}.jpg'}
            # POST request to take a picture
            post(picture_api_endpoint, json = picture_params_json)
            sleep(1)
        
        # JSON parameter list for video
        video_params_json = {'deviceID': f'{DEVICE_ID}', 'duration': 5, 'video_name': 'after_monitor_video.mp4'}
        print("INFO: taking after video")
        # POST request to take the video
        post(video_api_endpoint, json = video_params_json)
        
        
        # Wait till the PIR sensor stops sensing movement
        pir.wait_for_no_motion()
        print("INFO: motion stopped")

# Allow standalone testing of this module
if __name__ == "__main__":
    # Start motion detection loop
    motion_detect()
