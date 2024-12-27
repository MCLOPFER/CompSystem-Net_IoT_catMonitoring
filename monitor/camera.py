#!/usr/bin/python3

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
import cv2
from time import sleep

# Encountered issues with Glitch being far too slow to store media
#GLITCH_API_URL = "https://fluttering-linen-change.glitch.me/upload"  

# Created a class for the camera realted tasks so I could create a single,
# reusable camera object as I kept getting device in use errors
class camera:

    def __init__(self):
        self.
        # Single reusable camera instance 
        self.camera = Picamera2()
        pass
        

    def take_picture(self, deviceID, image_name):
        # ensure camera in stopped before attemting to configure it
        self.camera.stop()
        # configure the camera to take 1080p pictures
        camera_config = self.camera.create_still_configuration(main={"size": (1920, 1080)})
        self.camera.configure(camera_config)
        print("INFO: camera configured")
        # Create a dictionary
        data = {
            "deviceID": deviceID,
            "msg": ''
        }
        try:
            print("INFO: camera starting")
            self.camera.start()
            print("INFO: camera started")
            # Take the picture
            self.camera.capture_file(f"static/{image_name}")
            print(f"INFO: picture taken: static/{image_name}")
            # Initially wanted to use glitch but was too slow 
            # videos could take upto 6hrs for 10 second mp4
            #
            #if os.path.exists(f"static/{image_name}"):
            #    with open(f"static/{image_name}", encoding="utf8", errors='ignore') as img_file:
            #        print(f"INFO: uploading static/{image_name} to Glitch")
            #        response = post(GLITCH_API_URL, files={'file': img_file})
            #        print(response)
            #        httpBody=json.loads(response.text)
            #        data["msg"] = httpBody["url"]
            #else:
            #    data["msg"] = f"ERROR: Image not found: static/{image_name}"
            self.camera.stop()
        except Exception as e:
            data["msg"] = f"Failed to generate image, exception: {e}"
            self.camera.stop()
        return data
    
    def take_video(self,deviceID,duration,video_name):
        # ensure camera in stopped before attemting to configure it
        self.camera.stop()
        # configure the camera to take 1080p videos
        video_config = self.camera.create_video_configuration(main={"size": (1920, 1080)})
        self.camera.configure(video_config)
        # Create a dictionary
        data = {
            "deviceID": deviceID,
            "msg": ''
        }
        try:
            self.camera.start()
            encoder = H264Encoder(10000000)
            output = FfmpegOutput(f"static/{video_name}")
            # Start capturing video into the output file
            self.camera.start_recording(encoder, output)
            # wait for the disired recording length
            sleep(duration)
            # stop once the recording duration is met
            self.camera.stop_recording()
            data["msg"] = "Video generated"
            self.camera.stop()
        except Exception as e:
            data["msg"] = f"Failed to generate video, exception: {e}"
            self.camera.stop()
        return data
    
    def live_camera(self):
        # Create a preview configuration for live streaming
        self.camera.configure(self.camera.create_preview_configuration(main={"format": 'XRGB8888'}))
        self.camera.start()
        while True:
            # take image from next frame in the stream
            frame = self.camera.capture_array()
            # encode the image frame
            ret, buffer = cv2.imencode('.jpg', frame)
            # convert the encoded image frame to bytes
            frame = buffer.tobytes()
            # continously return new encoded image frame bytes
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



# Allow standalone testing of this module
if __name__ == "__main__":
    # Example device ID and usage
    deviceID = "test"
    camera = camera()
    image = camera.take_picture(deviceID, "test_image.jpg")
    # Print the data in JSON format for testing
    print(image)
    video = camera.take_video(deviceID,10,"test_video.mp4")
    # Print the data in JSON format for testing
    print(video)
    camera.camera.stop()
