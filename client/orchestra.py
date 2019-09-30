import paho.mqtt.client as mqtt

from psonic import *



# MQTT Settings
# ======================================================================================================================
class settings:
    pass


settings.broker = "test.mosquitto.org"
settings.broker_port = 1883
settings.topic = "FHNW2019"

# ======================================================================================================================



def on_connect(client, userdata, flags, rc):
    client.subscribe(settings.topic, 1)
    print('connected')

def on_message(client, userdata, message):

    msg = message.payload.decode("utf-8")
    ip, tone, synth = msg.split(';')
    print(ip, tone, synth)

    tone = 60


    if synth:
        use_synth(SAW)
    play(int(tone))



client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect

client.connect(settings.broker, settings.broker_port, 60)
client.loop_forever()


