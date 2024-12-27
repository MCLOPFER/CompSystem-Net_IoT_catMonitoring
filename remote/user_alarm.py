#!/usr/bin/python3

from pygame import mixer
from sense_hat import SenseHat
from time import sleep
from multiprocessing import Process

sense = SenseHat()

def user_alarm():
    sense.clear()
    # red
    r = (255,0,0)
    # light pink
    p = (255,105,180)
    # black
    b = (0,0,0)
    # white
    w = (255,255,255)
    border = [ b , r ]
    
    # Play alarm sound
    mixer.init()
    mixer.music.load("resources/alarm.wav")
    mixer.music.play(-1)
    mixer.music.get_busy()
    print("INFO: Alarm started.")

    alarm_status=True
    while alarm_status:
        for X in border:
            # light up a cat pattern with alternating border
            sense.set_pixels([X,X,X,X,X,X,X,X,
                              X,p,b,b,b,b,p,X,
                              X,p,w,b,b,w,p,X,
                              X,w,w,w,w,w,w,X,
                              X,w,b,w,w,b,w,X,
                              X,w,w,p,p,w,w,X,
                              X,b,w,w,w,w,b,X,
                              X,X,X,X,X,X,X,X,])
            sleep(0.25)
        # When the button on the sense hat
        for event in sense.stick.get_events():
            #  is pressed
            if event.action == "pressed":
                print("INFO: Alarm switched off.")
                #  switch off the alarm sound
                mixer.music.stop()
                sense.clear()
                alarm_status = False
                break
        continue

def sound_user_alarm(deviceID):
    data = {
        "deviceID": deviceID,
        "msg": ''
    }
    try:
        # start alarm in the background
        p = Process(target=user_alarm)
        p.start()
        data["msg"]="INFO: Alarm Started"
    except Exception as e:
        data["msg"] = f"ERROR: Fialed to start alarm with exception: {e}"
    return data

if __name__ == "__main__":
    msg = sound_user_alarm("test")
    print(str(msg))

