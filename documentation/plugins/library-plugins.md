# EasyTl documentation

## Library-plugins
Library-plugin - is plugin that provides functional for the developers. You can use it functional from any other plugin

**NOTE:** If you create the library-plugin, all functional you must place to the `namespace`!
Also, you can do `library-plugin namespace` in the `namespace`. Example plugin:
```python
# begin info
#   description = "Library-plugin | Adds simple myfunc()"
#   required_platforms = [ "windows", "linux", "android" ]
#   required_plugins = "no requirements"
#   etl_version_min = [ 1, 4, 0 ]
#   etl_version_max = [ 1, 4, "*" ]
#   version = "1.0.0"
#   update_link = "no link"
#   lang_links = "no link"
#   requirements = "no requirements"
#   author = "ftdot (https://github.com/ftdot)"
# end info

def myfunc(text):
    this.logger.info('myfunc() : ' + text)

namespace.mylib = namespace.Namespace()
namespace.mylib.myfunc = myfunc
```
Also note, that library-plugins must start with `1` to be loaded first than other plugins

## Library-plugin: 1STTLib
Provides the Speech To Text functional by using Google Recognition or Sphinx recognition APIs

**File: [src/plugins/1STTLib.plugin.py](../../src/plugins/1STTLib.plugin.py)**

>> ##### namespace.sttlib `Namespace`
>> Namespace of the library
>
>> ##### namespace.sttlib.recognizer `SpeechRecognition.Recognizer`
>> Instance of the Recognizer() from SpeechRecognition package
>
>> ##### namespace.sttlib.recognize_speech_from_file `(path: str, offline: bool = False, language: str = 'en-US') -> str`
>> Function that returns recognized text from audio file.
>>
>>> **Arguments:**
>>>
>>> `path: str` -- Path to the audio file
>>>
>>> `offline: bool` (default: False) -- Use offline recognizer ?
>>>
>>> `language: str` (default: 'en-US') -- Language to that be recognized the speech

## Library-plugin: 1TranslationsLib
Provides the text translation functional by using Google Translation API

**File: [src/plugins/1TranslationsLib.plugin.py](../../src/plugins/1TranslationsLib.plugin.py)**

>> ##### namespace.translatelib `Namespace`
>> Namespace of the library
>
>> ##### namespace.translatelib.translator `googletrans.Translator`
>> Instance of the Translator() from googletrans package
>
>> ##### namespace.translatelib.languages `dict[str, str]`
>> Available languages to translate.
>>
>> Key - language code
>>
>> Value - language name
>
>> ##### namespace.sttlib.translate `(text: str, to=Instance.translator.lang) -> str`
>> Translates any text to other language.
>> Wrapper to googletrans.Translator.translate().text
>>
>>> **Arguments:**
>>>
>>> path: str -- The text to be translated
>>>
>>> language: str (default: Instance.translator.lang, language of instance translator) -- The language (country code)
>
>> ##### namespace.sttlib.detect `(text: str) -> str`
>> Detects the language of the text,
>> Wrapper to googletrans.Translator.detect().lang
>>
>>> **Arguments:**
>>>
>>> path: str -- The text to be translated
>>>
>>> language: str (default: Instance.translator.lang, language of instance translator) -- The language (country code)