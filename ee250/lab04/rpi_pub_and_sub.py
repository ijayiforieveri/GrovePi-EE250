"""EE 250L Lab 04 Starter Code

Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import time
import sys
from grove_rgb_lcd import *
sys.path.append('../../Software/Python/grove_rgb_lcd')
import grovepi
dht_sensor_port = 7



def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("rpi-jaeishin/led")
    client.message_callback_add("rpi-jaeishin/led", ledcustom)
    #see line 29 for ledcustom functions
     
    client.subscribe("rpi-jaeishin/lcd")
    client.message_callback_add("rpi-jaeishin/lcd", lcdcustoms)
    #see line 37 for lcdcustom functions

    #subscribe to topics of interest here


#function of led customs for subscribing
def ledcustom(client, userdata, message):
    if str(message.payload, "utf-8") == "LED_ON":
       grovepi.digitalWrite(led, 1)
      
    else: 
       grovepi.digitalWrite(led, 0)

#function of lcd customs for subscribing
def lcdcustoms(client, userdata, message):
    if str(message.payload, "utf-8") == "w":
        setText_norefresh("w")
        
    elif str(message.payload, "utf-8") == "a":  
        setText_norefresh("a")
       
    elif str(message.payload, "utf-8") == "s":
        setText_norefresh("s")
        
    elif str(message.payload, "utf-8") == "d":  
        setText_norefresh("d")

    
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))
    print("on_message: msg.payload is of type " + str(type(msg.payload)))

 #Default message callback. Please use custom callbacks.

if __name__ == '__main__':

    PORT = 4
    led = 5
    button = 3
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        #flashes LCD screen to green
        setRGB(0,128,64)
        setRGB(0,255,0)
        ultrasonic = grovepi.ultrasonicRead(PORT)
        button_status = grovepi.digitalRead(button)
        #publish the ultrasonic range
        client.publish("rpi-jaeishin/ultrasonic", str(ultrasonic))
        print(ultrasonic)
        time.sleep(1)

        #when button is pressed publish button pressed
    if button_status:
        print("button pressed")
        client.publish("rpi-jaeishin/button", "Button pressed")



   
    
       
        
       

       


            

