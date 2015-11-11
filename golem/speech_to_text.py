from speech_recognition import UnknownValueError, Recognizer, WavFile
from golem.error import GolemException


def wav_to_text(wav_file_path, language="es-ES", show_all=False):
    r = Recognizer()
    with WavFile(wav_file_path) as source:
        audio = r.record(source)
    try:
        return r.recognize_google(audio_data=audio, language=language, show_all=show_all)
    except UnknownValueError:
        raise GolemException("Could not understand audio")
