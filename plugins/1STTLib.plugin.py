# begin info
#   description = "Library-plugin | (Speech To Text Lib) Provides functional to generate text from speech"
#   required_platforms = [ "windows", "linux", "android" ]
#   etl_version_min = [ 1, 3, 3 ]
#   etl_version_max = [ 1, 4, "*" ]
#   version = "1.0"
#   update_link = "no link"
#   lang_links = "no link"
#   requirements = [ "SpeechRecognition", "pydub" ]
#   author = "ftdot (https://github.com/ftdot)"
# end info

import os
import speech_recognition as sr
from pydub import AudioSegment

if 'ffmpeg' not in namespace.values or not namespace.values['ffmpeg']:
    this.logger.info('ffmpeg support is not enabled or not found')
    this.errored = True
    eee()

recognizer = sr.Recognizer()


def to_wav(path, output):
    x = AudioSegment.from_file(path)
    x.export(output, format='wav')


def recognize_speech_from_file(path: str, offline: bool = False, language: str = 'en') -> str:
    """Recognize speech to text from a file by the path

    :param path: Path to the audio file
    :type path: str
    :param offline: Use Sphnix engine isntead of the Google engine
    :type offline: bool
    :param language: Language (langcode) that be used to recognition
    :type language: str

    :return: Recognized text
    :rtype: str
    """

    try:
        if not (type_ := path.split('.'))[:-1] in ['wav', 'wave', 'aiff', 'flac']:
            path_ = os.path.join(namespace.instance.cache_dir, 'temp.wav')
            to_wav(path, path_)
            path = path_
    except Exception as e:
        this.log_exception(e)
        return '[STTLib] Can\'t recognize the speech! (When converting occurred an error)'

    with sr.AudioFile(path) as af:
        audio_data = namespace.sttlib.recognizer.record(af)

        return namespace.sttlib.recognizer.recognize_sphinx(audio_data, language=language) \
                    if offline else \
               namespace.sttlib.recognizer.recognize_google(audio_data, language=language)


# initialize sttlib namespace
namespace.values['sttlib'] = namespace.Namespace()
namespace.sttlib.recognizer = recognizer
namespace.sttlib.recognize_speech_from_file = recognize_speech_from_file