#!/usr/bin/python3

from flask import Flask, request, Response, render_template
from flask_cors import CORS
import os

import camera
# create an object of the camera class
camera = camera.camera()

#create Flask app instance and apply CORS
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'
CORS(app)

# route for taking a picture
@app.route('/camera/picture',methods=['POST'])
def picture():
    # parse inputted json into dict variable
    request_data = request.get_json()
    # setting variable from dict
    image_name = request_data['image_name']
    deviceID = request_data['deviceID']
    # call the take picture function on existing camera object
    data = camera.take_picture(deviceID,image_name)
    return data

# index route to display all before and after captured media in rendered template
@app.route('/') 
def index():
    # Set path to all media variables to load in the page
    after_video = os.path.join(app.config['UPLOAD_FOLDER'], 'after_monitor_video.mp4')
    after_image_0 = os.path.join(app.config['UPLOAD_FOLDER'], 'after_monitor_image_0.jpg')
    after_image_1 = os.path.join(app.config['UPLOAD_FOLDER'], 'after_monitor_image_1.jpg')
    before_image_0 = os.path.join(app.config['UPLOAD_FOLDER'], 'before_monitor_image_0.jpg')
    before_image_1 = os.path.join(app.config['UPLOAD_FOLDER'], 'before_monitor_image_1.jpg')    
    before_video = os.path.join(app.config['UPLOAD_FOLDER'], 'before_monitor_video.mp4')
    # render the output media
    return render_template('index.html', after_video=after_video, after_image_0=after_image_0, after_image_1=after_image_1, before_video=before_video, before_image_0=before_image_0, before_image_1=before_image_1)

# route for the live stream 
@app.route('/camera/live_stream')
def live_stream():
    return Response(camera.live_camera(), mimetype='multipart/x-mixed-replace; boundary=frame')

# route for the video recording API
@app.route('/camera/record',methods=['POST'])
def record():
    # parse inputted json into dict variable
    request_data = request.get_json()
    # setting variable from dict
    deviceID = request_data['deviceID']
    duration = request_data['duration']
    video_name = request_data['video_name']
    # call the take video function on existing camera object
    data = camera.take_video(deviceID,duration,video_name)
    return data

def start_camera_api():
    #Run API on port 5000
    app.run(host='0.0.0.0', port=5000, threaded=True)

if __name__ == "__main__":
    start_camera_api()
