#!/usr/bin/python
import paho.mqtt.client as mqtt
from subprocess import call
from sense_hat import SenseHat
import time


from settings import *

# generate soundwave
# ======================================================================================================================





client = mqtt.Client()
client.connect(settings.broker, settings.broker_port, 60)
client.subscribe(settings.topic, 1)
client.loop_start()


def on_message(client, userdata, message):
    if message.payload.decode("utf-8") == "off":
        sense = SenseHat()
        sense.show_message('Auf Wiedersehen', scroll_speed=0.1)
        time.sleep(10)
        call("sudo poweroff", shell=True)

client.on_message = on_message

while True:
    pass
