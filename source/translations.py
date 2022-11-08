import os.path
import tomllib
from .namespace import Namespace


class Translator:
    """Translator object provides the easy methods to translate text

    :param lang_dir: Path to the directory with the translation files
    :type lang_dir: str
    :param lang: Language (Country code)
    :type lang: str

    :ivar namespace: Instance of the Namespace
    :type namespace: Namespace
    """

    def __init__(self, lang_dir: str = os.path.join('.', 'lang'), lang: str = 'en'):
        self.lang_dir, self.lang = lang_dir, lang

        self.namespace = None

    @staticmethod
    def cyrillic(string: str):
        """Fixes cyrillic encoding problem

        :returns: Encoded string with UTF-8
        """

        return string.encode('1251').decode('utf8')

    def load_file(self, path: str):
        """(System method) Loads a file to the translations dictionary

        :param path: Path to the file
        :type path: str
        """

        self.namespace.instance.logger.debug('TRANSLATOR : Loading languages from the file by path '+path)

        n = os.path.basename(path)[:-8]
        with open(path, 'rb') as f:
            self.namespace.translations[n] = tomllib.load(f)

    def load_languages(self):
        """(System method) Loads the languages to the current languages dictionary"""

        # check for the translations dict in the namespace
        if 'translations' not in self.namespace.values:
            self.namespace.instance.logger.debug('TRANSLATOR : Create translations dict in the namespace')
            self.namespace.translations = {}

        files = [f for f in os.listdir(self.lang_dir) if f.endswith(self.lang+'.toml')]

        for f in files:
            self.load_file(os.path.join(self.lang_dir, f))

    def initialize(self, head: str):
        """Initializes the concrete translations file (loads it at the English language)

        :param head: Head of the translations file
        :type head: str
        """

        self.namespace.instance.logger.debug('TRANSLATOR : Initializing head ' + head)

        # check if head already in the dict
        if head in self.namespace.translations:
            self.namespace.instance.logger.debug('TRANSLATOR : Already initialized')
            return

        self.load_file(os.path.join(self.lang_dir, head+'_en.toml'))
