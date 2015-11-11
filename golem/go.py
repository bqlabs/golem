from golem.audio_recorder import record_to_file
import os
from golem.speech_to_text import wav_to_text
from golem.error import GolemException
from espeak import espeak
import socket
import json


if __name__ == '__main__':
    wav_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "voice.wav")
    mp3_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "voice.mp3")

    s = socket.socket()
    ip = "172.16.17.136"
    port = 5033
    s.connect((ip, port))
    while True:
        try:
            record_to_file(wav_file_path)
            text = wav_to_text(wav_file_path)
            x = 0
            y = 0
            w = 0
            print text
            if text == 'alante':
                x = 0.2
            if text == 'atrás'.decode('utf-8', 'ignore'):
                x = -0.2
            if text == 'derecha':
                y = 0.2
            if text == 'izquierda'.decode('utf-8', 'ignore'):
                y = -0.2
            print x, y
    #         espeak.set_voice('spanish')
    #         espeak.synth(text)
    #         while espeak.is_playing():
    #             pass
            s.send(json.dumps({'x': x,
                               'y': y,
                               'w': 0}))
        except GolemException:
            pass
        except KeyboardInterrupt:
            break

    s.send('quit')
    s.close()
