import time

import keyboard
import paho.mqtt.client as mqtt


# MQTT Settings
# ======================================================================================================================
class settings:
    pass


settings.broker = "test.mosquitto.org"
settings.broker_port = 1883
settings.topic = "FHNW2019"

client = mqtt.Client()
client.connect(settings.broker, settings.broker_port, 60)

client.loop_start()

while True:  # making a loop
    if keyboard.is_pressed('f'):  # iy 'q' is pressed
        client.publish(settings.topic, payload="snare", qos=0, retain=False)
    if keyboard.is_pressed('space'):  # if key 'space' is pressed
        client.publish(settings.topic, payload="hat", qos=0, retain=False)
    if keyboard.is_pressed('h'):  # if key 'h' is pressed
        client.publish(settings.topic, payload="kick", qos=0, retain=False)
    else:
        pass
    time.sleep(0.08)
