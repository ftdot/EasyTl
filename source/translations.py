import os.path
from configparser import ConfigParser
from .namespace import Namespace


class Translator:
    """Translator object provides the easy methods to translate text

    :param lang_dir: Path to the directory with the translation files
    :type lang_dir: str
    :param lang: Language (Country code)
    :type lang: str
    """

    def __init__(self, lang_dir: str = os.path.join('.', 'lang'), lang: str = 'en'):
        self.lang_dir, self.lang = lang_dir, lang

        self.translations = {}
        self.namespace = None

        self._cache = {}

    def load_file(self, path: str):
        """(System method) Loads a file to the translations dictionary

        :param path: Path to the file
        :type path: str
        """

        n = os.path.basename(path)[:-7]
        self.translations[n] = ConfigParser()
        self.translations[n].read(path)

    def load_language(self):
        """(System method) Loads the languages to the current languages dictionary"""

        files = [f for f in os.listdir(self.lang_dir) if f.endswith(self.lang+'.ini')]

        for f in files:
            self.load_file(os.path.join(self.lang_dir, f))

    def initialize(self, head: str):
        """Initializes the concrete translations file (loads it at the English language)

        :param head: Head of the translations file
        :type head: str
        """

        if head in self.translations:
            return
        self.load_file(os.path.join(self.lang_dir, head+'_en.ini'))

    def get(self, key: str) -> str:
        """Gets the translation string by the key in the translations dict

        :param key: Key (Format: [FILE HEAD].[HEADER].[KEY])
        :type key: str

        :returns: Translated string
        :rtype: str
        """

        if key in self._cache:
            return self._cache[key]

        path = key.split('.')
        value = self.translations
        for p in path:
            value = value[p]

        self._cache[key] = self.namespace.cyrillic(value)
        return self._cache[key]
