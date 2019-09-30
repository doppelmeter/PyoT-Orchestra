import paho.mqtt.client as mqtt

from psonic import *



# MQTT Settings
# ======================================================================================================================
class settings:
    pass


settings.broker = "test.mosquitto.org"
settings.broker_port = 1883
settings.topic = "FHNW2019"

# generate soundwave
# ======================================================================================================================





client = mqtt.Client()
client.connect(settings.broker, settings.broker_port, 60)
client.subscribe(settings.topic, 1)
client.loop_start()


def on_message(client, userdata, message):
    if message.payload.decode("utf-8") == "kick":
        play(60)
    elif message.payload.decode("utf-8") == "snare":
        play(40)
    elif message.payload.decode("utf-8") == "hat":
        play(100)


client.on_message = on_message

while True:
    pass

