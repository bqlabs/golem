# coding=utf-8

from golem.communication import audio_recorder
import os
from golem.communication.speech_to_text import wav_to_text
from golem.error import GolemException
from espeak import espeak
from golem.core.golem import Golem
from time import sleep


wav_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "voice.wav")


def speak(text):
    text = text.decode('utf8', 'ignore')
    text = text.encode('ascii', 'ignore')
    print text
    espeak.synth(text)
    while espeak.is_playing():
        pass
    sleep(0.1)


def config(golem):
    if not golem.id.name:
        try:
            while not golem.id.name:
                name = None
                speak('¿Como me llamo?')
                while True:
                    try:
                        audio_recorder.record_to_file(wav_file_path)
                        name = wav_to_text(wav_file_path)
                        print name
                        break
                    except GolemException:
                        speak('No te he entendido, ¿me lo repites?')
                print name
                while True:
                    try:
                        speak("Me llamo %s?" % name)
                        audio_recorder.record_to_file(wav_file_path)
                        text = wav_to_text(wav_file_path)
                        if text == 'sí'.decode('utf-8', 'ignore'):
                            golem.id.name = name
                            break
                        if text == 'No':
                            break
                    except GolemException:
                        speak('No te he entendido')
        except KeyboardInterrupt:
            return
    else:
        speak("%s despierto" % golem.id.name)


def golem(speaker=False):
    espeak.set_voice('spanish')
    golem = Golem()
    config(golem)
    speak('Me llamo %s' % golem.id.name)
    while True:
        try:
            audio_recorder.record_to_file(wav_file_path)
            text = wav_to_text(wav_file_path)
        except GolemException:
            pass
        except KeyboardInterrupt:
            break
    audio_recorder.close()

if __name__ == '__main__':
    golem()
