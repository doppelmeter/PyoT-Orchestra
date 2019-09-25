import paho.mqtt.client as mqtt

import pygame


# MQTT Settings
# ======================================================================================================================
class settings:
    pass


settings.broker = "test.mosquitto.org"
settings.broker_port = 1883
settings.topic = "FHNW2019"

# generate soundwave
# ======================================================================================================================


pygame.mixer.init(channels=8)

sound_snare = pygame.mixer.Sound("sounds/Snare 20.wav")
sound_kick = pygame.mixer.Sound("sounds/Kick_016.wav")
sound_hat = pygame.mixer.Sound("sounds/Closed Hat 08.wav")


def kick():
    pygame.mixer.Channel(5).play(sound_kick)
    pygame.mixer.Channel(3).set_volume(2)


def snare():
    pygame.mixer.Channel(1).play(sound_snare)


def hat():
    pygame.mixer.Channel(7).play(sound_hat, maxtime=250)
    pygame.mixer.Channel(7).set_volume(0.2)


client = mqtt.Client()
client.connect(settings.broker, settings.broker_port, 60)
client.subscribe(settings.topic, 1)
client.loop_start()


def on_message(client, userdata, message):
    if message.payload.decode("utf-8") == "kick":
        kick()
    elif message.payload.decode("utf-8") == "snare":
        snare()
    elif message.payload.decode("utf-8") == "hat":
        hat()


client.on_message = on_message

while True:
    pass

while False:
    kick()
    hat()
    time.sleep(0.3)
    hat()
    time.sleep(0.3)
    snare()
    kick()
    hat()
    time.sleep(0.3)
    hat()
    time.sleep(0.3)
