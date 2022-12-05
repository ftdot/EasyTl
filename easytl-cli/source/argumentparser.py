import logging
from .namespace import Namespace


class ArgumentParser:

    def __init__(self):
        self.instance_logger = logging.getLogger('EasyTl Instance')
        self.instance_logger.debug('Currently ArgumentParser is unavailable')

    def parse(self, args: list[str]) -> list[str]:
        self.instance_logger.debug('Currently ArgumentParser.parse() is unavailable, return list back')
        return args[1:]
