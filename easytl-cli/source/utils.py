import logging
import tomllib
import traceback
from enum import Enum

PLUGIN_INFO_PREFIX = '# '
utils_logger = logging.getLogger('EasyTl : Utils')


#####


class VersionCheckOperation(Enum):
    EQUALS = 'equals'
    LESS_THAN = 'less than'
    GREATER_THAN = 'greater than'


def _compare_values_is_equals(value1, value2):
    return value1 == '*' or value2 == '*' or value1 == value2


def _compare_values(value1, value2, func):
    if not getattr(value1, func)(value2):
        if not value1 == value2:
            return False, False
        return True, True
    return True, False


def _compare_values_less_than(value1, value2):
    return _compare_values(value1, value2, '__lt__')


def _compare_values_greater_than(value1, value2):
    return _compare_values(value1, value2, '__gt__')


# Checks the types of the values
def _check_types(value1: int | str, value2: int | str) -> (bool, str | int, str | int):
    """Does type-casting of the given values

    :param value1: First value
    :type value1: int | str
    :param value2: Second value
    :type value2: int | str

    :return: Returns a tuple with values (ERROR, first value type-casted, second value type-casted
    :rtype: (bool, int | str, int | str)
    """

    def _check_type(value: int | str):
        if value == '*' or isinstance(value, int):
            return value
        elif isinstance(value, str) and value.isnumeric():
            return int(value)
        else:
            utils_logger.debug('_check_types._check_type() : '
                                'First value is can\'t be type-casted. Return with the error')
            return None

    return (False, value_tc1, value_tc2) \
        if all((value_tc1 := (_check_type(value1[0]), _check_type(value1[1]), _check_type(value1[2])),
                value_tc2 := (_check_type(value2[0]), _check_type(value2[1]), _check_type(value2[2]))
                )) \
        else (True, None, None)


#####


def check_version_compatibility(
        version1: tuple[int | str, int | str, int | str] | list[int | str, int | str, int | str],
        version2: tuple[int | str, int | str, int | str] | list[int | str, int | str, int | str],
        operation: VersionCheckOperation | str = VersionCheckOperation.EQUALS) -> bool:
    """Compares the two versions

    :param version1: A first version example
    :type version1: tuple[int | str, int | str, int | str] | list[int | str, int | str, int | str]
    :param version2: The second version example
    :type version2: tuple[int | str, int | str, int | str] | list[int | str, int | str, int | str]
    :param operation: An operations, that be applied to these versions instance
    :type operation: VersionCheckOperation | str

    :return: True if the expression is right, otherwise False
    :rtype: bool
    """
    result = []

    err, version1, version2 = _check_types(version1, version2)

    if err:
        utils_logger.debug('function utils.check_version_compatibility() : _check_types() returned error')
        return False

    match operation:
        case VersionCheckOperation.EQUALS:
            if not (_compare_values_is_equals(version1[0], version2[0])
                    and _compare_values_is_equals(version1[1], version2[1])
                    and _compare_values_is_equals(version1[2], version2[2])):
                return False
        case VersionCheckOperation.LESS_THAN:
            major_equals = False
            minor_equals = False

            not_lt, major_equals = _compare_values_less_than(version1[0], version2[0])
            if not not_lt:
                return False

            not_lt, minor_equals = _compare_values_less_than(version1[1], version2[1])
            if not not_lt:
                return False

            if (major_equals and minor_equals) and \
                    not (version1[2] == '*' or version2[2] == '*'
                         or version1[2] < version2[2]):
                return False
        case VersionCheckOperation.GREATER_THAN:
            major_equals = False
            minor_equals = False

            not_lt, major_equals = _compare_values_greater_than(version1[0], version2[0])
            if not not_lt:
                return False

            not_lt, minor_equals = _compare_values_greater_than(version1[1], version2[1])
            if not not_lt:
                return False

            if (major_equals and minor_equals) and \
                    not (version1[2] == '*' or version2[2] == '*'
                         or version1[2] > version2[2]):
                return False

        case _:
            utils_logger.debug('function utils.check_version_compatibility() : Incorrect operation was set')
            return False

    return True

####


def parse_plugin_information(file_lines: list[str]) -> (bool, dict):
    """Parses the information about the plugin in TOML format

    :param file_lines: List with the file lines separated by newline
    :type file_lines: list[str]

    :return: True or False as first value - it detects if plugin has info lines v2 format. (will be deleted in 1.5+)
             Second value - TOML dict with the information about the plugin
    :rtype: (bool, dict)
    """

    utils_logger.debug('utils.parse_plugin_information() : '
                        'Start parsing the info lines')

    v2_format = False

    begin = False
    toml_lines = ""

    for line in file_lines:
        if line.startswith(PLUGIN_INFO_PREFIX + 'begin info'):
            v2_format = True
            begin = True

            utils_logger.debug('utils.parse_plugin_information() : '
                                'Found a begin of info line')

        elif line.startswith(PLUGIN_INFO_PREFIX + 'end info'):
            begin = False

            utils_logger.debug('utils.parse_plugin_information() : '
                                'Found the end of info line')
        else:
            if begin:
                utils_logger.debug('utils.parse_plugin_information() : '
                                    'Add TOML line : ' + (toml_line := line.removeprefix(PLUGIN_INFO_PREFIX + ' ')))
                toml_lines += toml_line + '\n'

    utils_logger.debug('utils.parse_plugin_information() : '
                        'Plugin is v2_format? : ' + 'yes' if v2_format else 'no')

    for line in toml_lines.split('\n'):
        utils_logger.debug('utils.parse_plugin_information() : '
                            'TOML LINES : ' + line)

    return v2_format, tomllib.loads(toml_lines)

####

error_splitter = '#' * 25


def log_exception(logger: logging.Logger, e: Exception):
    """Logs the exception to the logger

    :param logger: Logger instance
    :type logger: logging.Logger
    :param e: Exception to be logged
    :type e: Exception
    """

    logger.debug(error_splitter)

    logger.error('Exception has been generated, while executing the plugin')
    for line in traceback.format_exception(e):
        logger.debug(line.removesuffix('\n'))

    logger.debug(error_splitter)
