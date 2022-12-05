# begin info
#   description = "Library-plugin | (Speech To Text Lib) Provides functional to generate text from speech"
#   required_platforms = [ "windows", "linux", "android" ]
#   required_plugins = "no requirements"
#   etl_version_min = [ 1, 4, 0 ]
#   etl_version_max = [ 1, 4, "*" ]
#   version = "1.2"
#   update_link = "https://github.com/ftdot/EasyTl/raw/master/easytl-cli/plugins/1STTLib.plugin.py"
#   lang_links = "no link"
#   requirements = [ "SpeechRecognition", "pydub", "pocketsphinx" ]
#   author = "ftdot (https://github.com/ftdot)"
#   changelog = [ "Support for the 1.4.0 version" ]
# end info

import os
import speech_recognition as sr
from pydub import AudioSegment
from source.exceptions import PluginRequiresError

if 'ffmpeg' not in dir(namespace) or not namespace.ffmpeg:
    this.logger.info('ffmpeg support is not enabled or not found')
    this.errored = True

    raise PluginRequiresError(this.plugin_name, 'bin: ffmpeg')

recognizer = sr.Recognizer()


def to_wav(path, output):
    x = AudioSegment.from_file(path)
    x.export(output, format='wav')


def recognize_speech_from_file(path: str, offline: bool = False, language: str = 'en-US') -> str:
    """Recognize speech to text from a file by the path

    :param path: Path to the audio file
    :type path: str
    :param offline: Use Sphinx engine instead of the Google engine
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
namespace.sttlib = namespace.Namespace()
namespace.sttlib.recognizer = recognizer
namespace.sttlib.recognize_speech_from_file = recognize_speech_from_file
