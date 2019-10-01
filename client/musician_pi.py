#!/usr/bin/python
from sense_hat import SenseHat
import time
import subprocess
import paho.mqtt.client as mqtt
from utils.functions import get_ip_adress
from utils.display import triangel, piano, guitar, attention
from utils.settings import *


ip_adress = get_ip_adress()



client = mqtt.Client()
client.connect(settings.broker, settings.broker_port, 60)

client.loop_start()

# Tonleiter und Instrument auswählen
# ======================================================================================================================
sense = SenseHat()
# Tonleiter
scale = ["C", "D", "E", "F", "G", "A", "H"]
# Instrumente


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
