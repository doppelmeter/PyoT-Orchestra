# MQTT Settings
# ======================================================================================================================
class settings:
    pass


settings.broker = "test.mosquitto.org"
settings.broker_port = 1883
settings.topic = "FHNW2019"
settings.topic_sound_msg = settings.topic + "/sound-msg"
settings.topic_control_orchestra = settings.topic + "/ctl-orchestra"
settings.topic_admin = settings.topic + "/admin"

settings.sound_param = {
    'attack': None,
    'decay': None,
    'sustain_level': None,
    'sustain': None,
    'release': None,
    'cutoff': None,
    'cutoff_attack': None,
    'amp': None,
    'pan': None
}