#!/usr/bin/python3

from flask import Flask
from flask_cors import CORS
from multiprocessing import Process
from user_alarm import sound_user_alarm

deviceID="user_remote"

#create Flask app instance and apply CORS
app = Flask(__name__)
CORS(app)

@app.route('/trigger_user_alarm',methods=['GET'])
def trigger_user_alarm():
    data = sound_user_alarm(deviceID)
    return data["msg"]+"\n"

def start_user_alarm_api():
    #Run API on port 5000
    app.run(host='0.0.0.0', port=5000, threaded=True)

def start_backround_user_alarm_api():
    try:
        # start alarm api flask app in the background
        p = Process(target=start_user_alarm_api)
        p.start()
        print("INFO: User alarm api server started")
    except Exception as e:
        print(f"ERROR: Fialed to start alarm api server with exception: {e}")

if __name__ == "__main__":
    print("INFO: local testing of user alarm api")
    start_user_alarm_api()