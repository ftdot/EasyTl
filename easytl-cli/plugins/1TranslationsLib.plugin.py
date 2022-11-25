# begin info
#   description = "Library-plugin | Allows to other plugins use translating"
#   required_platforms = [ "windows", "linux", "android" ]
#   etl_version_min = [ 1, 3, 3 ]
#   etl_version_max = [ 1, 4, "*" ]
#   version = "1.2"
#   update_link = "https://github.com/ftdot/EasyTl/raw/master/plugins/1TranslationsLib.plugin.py"
#   lang_links = "no link"
#   requirements = [ [ "googletrans", "googletrans==4.0.0-rc1" ] ]
#   author = "ftdot (https://github.com/ftdot)"
#   changelog = [ "Added `namespace.translatelib.translator`", "requirements fix for the 1.3.3-beta version" ]
# end info

import googletrans

# settings
default_translate_to = namespace.instance.translator.lang

# initialize the Google translator
translator = googletrans.Translator()


def translate(text: str, to=default_translate_to) -> str:
    """Translates any text to other language.
    Wrapper to googletrans.Translator.translate().text

    :param text: The text to be translated
    :type text: str
    :param to: The language (country code)
    :type to: str

    :returns: Translated text
    :rtype: str
    """

    return namespace.translatelib.translator.translate(text, dest=to).text


def detect(text: str) -> str:
    """Detects the language of the text.
    Wrapper to googletrans.Translator.detect()

    :param text: The text to detect the language
    :type text: str

    :returns: Country code of language
    :rtype: str
    """

    return namespace.translatelib.translator.detect(text).lang

# initializing translatelib namespace
namespace.translatelib = namespace.Namespace()

# add functions to translatelib namespace
namespace.translatelib.translate = translate
namespace.translatelib.translator = translator
namespace.translatelib.languages = googletrans.LANGUAGES
