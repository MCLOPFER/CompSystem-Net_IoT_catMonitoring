<p align="center">
  <img src="images/three_kittens.png"/>
</p>

# Kitten Monitor
#### Student Name: *MariCruz Lopez*   Student ID: *20108907*

## Problem
I have recently got 3 kittens and they are wreaking havoc in my house while I am not there.

## Solution
I am going to create a monitoring/CCTV system using two Raspberry Pi's.

The first will be placed in the laundry room to monitor if the kittens enter the room, using a Camera triggered with a motion sensor.

The second will be kept with me in the spare bedroom where I am studying and will be equipped with a SenseHAT to notify me, by lighting up the SenseHAT LED's and playing an audio notification, if I respond to the the notification locally by acknowledging it via the button on the SenseHAT nothing will occur, if I miss the notification I will be sent an email alert from Thingspeak(as it is assumed I am away from home).

Once I review the events in Thingspeak after the alert I will add an option to sound an alarm in the laundry room if I am away from home to hopefully scare the intruders(kittens) out of the laundry room.

## Tools, Technologies and Equipment

I aim to use a combination of MQTT and ThingSpeak to achieve this by using them to notify me via email or phone notification(via an MQTT client app) if motion has been detected in the laundry room and allow me to review pictures taken at the motion detection event and sound an alarm if needed.

I plan to use two Raspberry Pi's, a high definition camera module with tripod, a SenseHAT and a pair of wired audio jack speakers to sound notifications and alarms.

## Project Repository
https://github.com/MCLOPFER/CompSystem-Net_IoT_catMonitoring

