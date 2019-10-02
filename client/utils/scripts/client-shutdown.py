#!/usr/bin/python

# ToDo: Refactor/Redesign workflow to turn of pi's
# ToDo: Error in script, it can't access the utils-package therefore
exit()

#
import time
from subprocess import call

import paho.mqtt.client as mqtt
from sense_hat import SenseHat
from utils.settings import *

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
