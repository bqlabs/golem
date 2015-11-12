# coding=utf-8

from golem.communication import audio_recorder
import os
from golem.communication.speech_to_text import wav_to_text
from golem.error import GolemException
from golem.communication.language_processor import TextProccess
from espeak import espeak
from golem.core.golem import Golem
from time import sleep


wav_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "voice.wav")


def speak(text):
    espeak.synth(text)
    while espeak.is_playing():
        pass
    sleep(0.1)


def golem(speaker=False):
    print "Despertando al Golem ...\n\n"
    espeak.set_voice('spanish')
    text_proccess = TextProccess()
    speak("Golem despierto")
    golem = Golem()
    while not golem.name:
        try:
            speak('Como me llamo?')
            audio_recorder.record_to_file(wav_file_path)
            text = wav_to_text(wav_file_path)
            result = text_proccess.text_proccess(text)
            if not golem.name:
                golem.name = text
        except GolemException:
            pass
        except KeyboardInterrupt:
            break
    speak('Me llamo %s' % golem.name)
    while True:
        try:
            audio_recorder.record_to_file(wav_file_path)
            text = wav_to_text(wav_file_path)
            result = text_proccess.text_proccess(text)
            print result
            # 'option'.decode('utf-8', 'ignore'):
            if speaker:
                speak(text)
        except GolemException:
            pass
        except KeyboardInterrupt:
            break
    audio_recorder.close()

if __name__ == '__main__':
    golem()
