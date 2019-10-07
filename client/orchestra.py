import json
import subprocess

import paho.mqtt.client as mqtt
from psonic import *

from utils.settings import *

# extends / set settings
# ======================================================================================================================
settings.output_commandline = False  # not recommended to change, sonic-pi-pipe has to be installed
settings.command_powershell = r'powershell'
settings.active_loops_synths = []

settings.sound_param['release'] = 0.5

# generate Lookup dict for notes
# ======================================================================================================================
root_notes = {
    "C0": 12,
    "Cs0": 13,
    "Db0": 13,
    "D0": 14,
    "Ds0": 15,
    "Eb0": 15,
    "E0": 16,
    "F0": 17,
    "Fs0": 18,
    "Gb0": 18,
    "G0": 19,
    "Gs0": 20,
    "Ab0": 20,
    "A0": 21,
    "As0": 22,
    "Bb0": 22,
    "B0": 23,
}

notes = {}
for octave in range(9):
    for key in root_notes:
        notes[key.replace("0", str(octave))] = root_notes[key] + (12 * octave)

# generate Lookup dict for synthesizers
# ======================================================================================================================
synths = {}

synths['dull_bell'] = DULL_BELL
synths['pretty_bell'] = PRETTY_BELL
synths['sine'] = SINE
synths['square'] = SQUARE
synths['pulse'] = PULSE
synths['subpulse'] = SUBPULSE
synths['dtri'] = DTRI
synths['dpulse'] = DPULSE
synths['fm'] = FM
synths['mod_fm'] = MOD_FM
synths['mod_saw'] = MOD_SAW
synths['mod_dsaw'] = MOD_DSAW
synths['mod_sine'] = MOD_SINE
synths['mod_tri'] = MOD_TRI
synths['mod_pulse'] = MOD_PULSE
synths['supersaw'] = SUPERSAW
synths['hoover'] = HOOVER
synths['synth_violin'] = SYNTH_VIOLIN
synths['pluck'] = PLUCK
synths['piano'] = PIANO
synths['growl'] = GROWL
synths['dark_ambience'] = DARK_AMBIENCE
synths['dark_sea_horn'] = DARK_SEA_HORN
synths['hollow'] = HOLLOW
synths['zawa'] = ZAWA
synths['noise'] = NOISE
synths['gnoise'] = GNOISE
synths['bnoise'] = BNOISE
synths['cnoise'] = CNOISE
synths['dsaw'] = DSAW
synths['tb303'] = TB303
synths['blade'] = BLADE
synths['prophet'] = PROPHET
synths['saw'] = SAW
synths['beep'] = BEEP
synths['tri'] = TRI
synths['chiplead'] = CHIPLEAD
synths['chipbass'] = CHIPBASS
synths['chipnoise'] = CHIPNOISE
synths['techsaws'] = TECHSAWS
synths['sound_in'] = SOUND_IN
synths['sound_in_stereo'] = SOUND_IN_STEREO


# define functions
# ======================================================================================================================
def define_sonicpi_loop(synth="piano"):
    command = f"live_loop :l_{synth} do\n" \
              "use_real_time\n" \
              f"a,b=sync '/osc/trigger/{synth}'\n" \
              f"synth :{synth}, note: a, release: b\n" \
              "end"

    run(command)


# MQTT-subscriber and sound generator
# ======================================================================================================================

def on_connect(client, userdata, flags, rc):
    client.subscribe(settings.topic_sound_msg, 1)
    client.subscribe(settings.topic_control_orchestra)
    print('connected to ' + settings.broker)


def on_message(client, userdata, message):
    """
    message expects: '127.0.0.1;C4;tri':
    """
    if message.topic == settings.topic_sound_msg:

        try:
            msg = message.payload.decode("utf-8")

            ip, note, synth = msg.split(';')
            midi = int(notes[note.capitalize()])

            if not settings.output_commandline:

                if synth not in synths:
                    synth = "piano"

                if synth not in settings.active_loops_synths:
                    define_sonicpi_loop(synth)
                    settings.active_loops_synths.append(synth)
                    print("Loop defined for synth ", synth)
                    time.sleep(0.5)

                send_message(f'/trigger/{synth}', midi, settings.sound_param["release"])

            else:
                command = r'echo "play ' + str(midi) + '" | sonic-pi-pipe'
                print(command)
                subprocess.Popen([settings.command_powershell, command],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, shell=True)


        except:
            print(
                'Could not process message ' + message.payload.decode('utf-8') + ' @ topic ' + settings.topic_sound_msg)


    elif message.topic == settings.topic_control_orchestra:
        try:
            msg = message.payload.decode("utf-8", "ignore")
            msg_dict = json.loads(msg)
            print(msg_dict)

            for key, value in msg_dict.items():
                if key in settings.sound_param:
                    settings.sound_param[key] = value
                    print("Sound parameter changed: ", key, value)
                else:
                    print("unexpected parameter", key, value)
        except:
            print('Could not process message ' + message.payload.decode(
                'utf-8') + ' @ topic ' + settings.topic_control_orchestra)


client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect

client.connect(settings.broker, settings.broker_port, 60)
client.loop_forever()
