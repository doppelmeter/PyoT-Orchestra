#!/usr/bin/python
from sense_hat import SenseHat
import time
import socket
import subprocess
import paho.mqtt.client as mqtt


# IP-Adresse
# ======================================================================================================================
def get_ip_adress():
    ip_address = '';
    connected = False
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while not connected:
        connected = True
        try:
            s.connect(("8.8.8.8", 80))
        except:
            connected = False

    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

ip_adress = get_ip_adress()

from settings import *

client = mqtt.Client()
client.connect(settings.broker, settings.broker_port, 60)

client.loop_start()

# Tonleiter und Instrument auswählen
# ======================================================================================================================
sense = SenseHat()
# Tonleiter
scale = ["C", "D", "E", "F", "G", "A", "H"]
# Instrumente
black = (0,0,0)
r = (255,0,0)
g = (0,255,0)
y = (255,255,0)
gray = (180, 180, 180)
b = (0,0,255)
w =(255,255,255)
triangel = [g,g,g,g,g,g,g,g,
            g,g,g,g,g,g,g,g,
            g,g,g,w,g,g,g,g,
            g,g,w,g,w,g,g,g,
            g,w,g,g,g,w,g,g,
            w,w,w,w,w,w,w,g,
            g,g,g,g,g,g,g,g,
            g,g,g,g,g,g,g,g]

piano =    [g,g,g,g,g,g,g,g,
            g,g,g,g,g,g,g,g,
            gray,black,gray,black,gray,black,gray,black,
            gray,black,gray,black,gray,black,gray,black,
            gray,gray,gray,gray,gray,gray,gray,gray,
            gray,gray,gray,gray,gray,gray,gray,gray,
            g,g,g,g,g,g,g,g,
            g,g,g,g,g,g,g,g]

guitar =   [w,g,g,g,g,g,g,g,
            g,w,g,g,g,g,g,g,
            g,g,w,g,w,w,g,g,
            g,g,g,w,w,w,w,g,
            g,g,g,w,w,w,w,g,
            g,g,g,w,w,w,w,g,
            g,g,g,g,w,w,g,g,
            g,g,g,g,g,g,g,g]

synt = [triangel, piano, guitar]

current_synt = 0
current_tones = 0
octave = 5

def define_tones_synt(current_tones, current_synt, octave):
    if event.direction == "up":
        current_tones += 1
        if current_tones >= len(scale):
            current_tones = 0
            octave += 1
            if octave > 8:
                octave = 0
        sense.show_letter(str(scale[current_tones]))

    elif event.direction == "down":
        current_tones -= 1
        if current_tones < 0:
            current_tones = len(scale)-1
            octave -= 1
            if octave < 0:
                octave = 8
        sense.show_letter(str(scale[current_tones]))

    elif event.direction == "right":
        current_synt += 1
        if current_synt >= len(synt):
            current_synt = 0
            octave += 1
            if octave > 8:
                octave = 0
        sense.set_pixels(synt[current_synt])

    elif event.direction == "left":
        current_synt -= 1
        if current_synt < 0:
            current_synt = len(synt)-1
            octave -= 1
            if octave < 0:
                octave = 8
        sense.set_pixels(synt[current_synt])
    
    return current_tones, current_synt, octave


def hit():
    acceleration = sense.get_accelerometer_raw()
    #x = acceleration['x']
    #y = acceleration['y']
    z = acceleration['z']
    return abs(z)

attention =     [r,r,r,y,y,r,r,r,
                r,r,r,y,y,r,r,r,
                r,r,r,y,y,r,r,r,
                r,r,r,y,y,r,r,r,
                r,r,r,r,r,r,r,r,
                r,r,r,y,y,r,r,r,
                r,r,r,y,y,r,r,r,
                r,r,r,r,r,r,r,r]
def temp():
    temp = sense.get_temperature()
    return temp


while True:
    # Tonhöhe und Klangemdium auswählen
    for event in sense.stick.get_events():
        # Check if the joystick was pressed
        if event.action == "pressed":
            current_tones, current_synt, octave = define_tones_synt(current_tones, current_synt,octave)
            
    # Test auf Schüttelbewegung > 1.5g in z-Richtung, Senden an Broker bei
    if hit() > 1.5:
        sense.show_letter("X")
        send = f"{ip_adress};{scale[current_tones]}{octave};{current_synt}"
        client.publish(settings.topic, payload=send, qos=0, retain=False)
        time.sleep(0.1)
        sense.clear()

    if temp() > 50:
        sense.set_pixels(attention)
        # Pi ausschalten in 5s
        subprocess.Popen(['shutdown', '-h', '-t 5'])
        break


    time.sleep(0.08)
