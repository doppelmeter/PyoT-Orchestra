import paho.mqtt.client as mqtt
import subprocess

from psonic import *

from utils.settings import *

# extends / set settings
# ======================================================================================================================
settings.tone_release = 1
settings.output_commandline = False # not recommended to change
settings.command_powershell = r'powershell'

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


# MQTT-subscriber and sound generator
# ======================================================================================================================

def on_connect(client, userdata, flags, rc):
    client.subscribe(settings.topic_sound_msg, 1)
    print('connected to ' + settings.broker)


def on_message(client, userdata, message):
    """
    message expects: '127.0.0.1;C4;tri':
    """
    try:
        msg = message.payload.decode("utf-8")

        ip, note, synth = msg.split(';')
        midi = int(notes[note.capitalize()])

        if not settings.output_commandline:

            if synth.lower() in synths:
                use_synth(synths[synth.lower()])
            else:
                use_synth(PIANO)

            play(midi, attack=settings.sound_param['attack'], decay=settings.sound_param['decay'],
                 sustain_level=settings.sound_param['sustain_level'], sustain=settings.sound_param['sustain'],
                 release=settings.sound_param['release'], cutoff=settings.sound_param['cutoff'],
                 cutoff_attack=settings.sound_param['cutoff_attack'], amp=settings.sound_param['amp'],
                 pan=settings.sound_param['pan'])

        else:
            command = r'echo "play ' + str(midi) + '" | sonic-pi-pipe'
            print(command)
            subprocess.Popen([settings.command_powershell, command],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, shell=True)

    except:
        print('Could not process message ' + message.payload.decode('utf-8'))


client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect

client.connect(settings.broker, settings.broker_port, 60)
client.loop_forever()
