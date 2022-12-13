import logging
from .namespace import Namespace
from .utils import log_exception
from .exceptions import ArgumentTypeCastingError
from typing import Any
from enum import Enum, auto

# symbols to escape
escape_dict = {
    '"': '"',
    "'": "'"
}


class ArgumentParseError(Enum):
    TooMuchArguments    = auto()
    TooLittleArguments  = auto()
    IncorrectType       = auto()


class ArgTypeCast:
    """Base class to help with the type-casting"""

    def __init__(self, type_: type):
        """
        :param type_: Type for the type-casting
        :type type_: type
        """
        self.type = type_

    def typecast(self, string: str) -> Any:
        """Type-cast string to the given type

        :param string: String to be type-casted
        :type string: str

        :return: Type-casted object
        :rtype: Any
        """

        return self.type(string)


class ListCast(ArgTypeCast):
    """Type-cast a string to the list"""

    def __init__(self, splitter: str = ', ', values_type: ArgTypeCast = ArgTypeCast(str)):
        """
        :param splitter: String splitter
        :type splitter: str
        :param values_type: Type to cast the values of the list
        :type values_type: ArgTypeCast
        """
        super().__init__(list)

        self.splitter = splitter
        self.values_type = values_type

    def typecast(self, string: str) -> list[str]:
        """Type-cast string to the list

        :param string: String to be type-casted
        :type string: str

        :return: Type-casted list object
        :rtype: list
        """

        return [self.values_type.typecast(v) for v in string.split(self.splitter)]


class DictCast(ArgTypeCast):
    """Type-cast a string to the dict"""

    def __init__(self,
                 splitter: str = ',',
                 kv_splitter: str = '=',
                 temp_char: str = '\uFFFF',
                 key_type: ArgTypeCast = ArgTypeCast(str),
                 values_type: ArgTypeCast = ArgTypeCast(str)):
        """
        :param splitter: Splitter to split the (key=value) pairs
        :type splitter: str
        :param kv_splitter: Splitter to split the key and value
        :type kv_splitter: str
        :param temp_char: Temp char to replace the '==' with it and back
        :type temp_char

        :param key_type: Type to type-cast the keys
        :type key_type: ArgTypeCast
        :param values_type: Type to type-cast the values
        :type values_type: ArgTypeCast
        """
        super().__init__(dict)

        self.splitter = splitter
        self.kv_splitter = kv_splitter
        self.temp_char = temp_char

        self.key_type = key_type
        self.values_type = values_type

    def typecast(self, string: str) -> dict[Any, Any]:
        """Type-cast string to the dict

        :param string: String to be type-casted
        :type string: str

        :return: Type-casted dict object
        :rtype: dict[Any, Any]
        """
        temp_cast = string.replace('==', self.temp_char)
        return {
            self.key_type.typecast((kvs := kv.split(self.kv_splitter))[0]):
                self.values_type.typecast(kvs[1].replace(self.temp_char, '=='))
            for kv in temp_cast.split(self.splitter)
        }


# define for the BoolCast
_true_list = ['yes', 'yea', '+', 'true']
_false_list = ['no', 'nop', '-', 'false']


class BoolCast(ArgTypeCast):
    """Type-cast a string to the bool"""

    def __init__(self, true_list: list[str] | None = None, false_list: list[str] | None = None,
                 match_case: bool = False):
        """
        :param true_list: List with the true string variants
        :type true_list: list[str]
        :param false_list: List with the false string variants
        :type false_list: list[str]
        :param match_case: Match case of the string
        :type match_case: bool
        """
        super().__init__(dict)

        self.true_list = true_list if true_list is not None else _true_list
        self.false_list = false_list if false_list is not None else _false_list
        self.match_case = match_case

    def typecast(self, string: str) -> bool:
        """Type-cast string to the given type

        :param string: String to be type-casted
        :type string: str

        :return: Type-casted bool object
        :rtype: bool

        :raises ArgumentTypeCastingError: When string isn't have in the true\false list
        """

        string_to_parse = string if self.match_case else string.lower()

        if string_to_parse in self.true_list:
            return True
        elif string_to_parse in self.false_list:
            return False
        else:
            raise ArgumentTypeCastingError(f'Can\'t type cast the string "{string}" to bool')


# define the type-casts
class Cast:
    StrCast = ArgTypeCast(str)
    IntCast = ArgTypeCast(int)
    FloatCast = ArgTypeCast(float)
    BoolCast = ArgTypeCast(bool)


class ListCastEnum:
    ListStrCast = ListCast()
    ListIntCast = ListCast(values_type=Cast.IntCast)
    ListFloatCast = ListCast(values_type=Cast.FloatCast)
    ListBoolCast = ListCast(values_type=Cast.BoolCast)


class ListDictEnum:
    DictStrStrCast = DictCast()
    DictStrIntCast = DictCast(values_type=Cast.IntCast)
    DictStrFloatCast = DictCast(values_type=Cast.FloatCast)
    DictStrBoolCast = DictCast(values_type=Cast.BoolCast)


class Argument:
    """Sample argument"""

    def __init__(self,
                 arg_name: str,
                 arg_type: ArgTypeCast = Cast.StrCast,
                 default: Any | None = None,
                 description: str = 'Sample argument'
                 ):
        """
        :param arg_name: Name of the argument
        :type arg_name: str
        :param arg_type: Type of the argument (NOTE: It must support type-casting with using str)
        :type arg_type: type
        :param default: Defines default value of the argument. If it None - argument is marked as required
        :type default: Any | None
        :param description: Description of the argument
        :type description: str
        """

        self.arg_name = arg_name
        self.arg_type = arg_type
        self.default = default
        self.description = description

        self.is_optional = self.default is not None

    def typecast(self, input_arg: str) -> (bool, Exception | Any):
        """Try to type-cast the string argument to the argument type

        :param input_arg: Input argument in the str type
        :type input_arg: str

        :return: Tuple with bool ERROR, type-casted object or Exception if ERROR is True
        :rtype: (bool, Exception | Any)
        """

        try:
            return False, self.arg_type.typecast(input_arg)
        except Exception as e:
            return True, e


class ArgumentParser:
    """Helps to manage the arguments"""

    def __init__(self, parent_plugin, arguments: list[Argument]):
        """
        :param parent_plugin: Parent plugin of this parser
        :type parent_plugin: Plugin
        :param arguments: List with the arguments
        :type arguments: list[Argument]
        """
    
        self.parent_plugin = parent_plugin
        self.arguments = arguments

        self.logger = logging.getLogger('EasyTl : ArgumentParser')

        self.logger.debug('Initializing the values')
        self.position_arguments = 0
        self.default_arguments = 0

        for arg in self.arguments:
            if arg.default:
                self.default_arguments += 1
                continue

            self.position_arguments += 1

    async def parse(self, args: list[str]) -> (bool, Namespace | ArgumentParseError):
        self.logger.debug('Logger called with arguments list: ' + ', '.join(args))

        # initialize the variables
        output_args = Namespace()
        output_args.PREFIX = args[0]
        output_args.CMD = args[1]
        input_str = ' '.join(args[2:]) + '\00'

        # initialize the variables to first parse stage
        str_open = False
        temp_str = ''
        temp_args = []
        escaped = False

        # first parse stage (strings with spaces, escaping)
        for s in input_str:
            if escaped:
                if s not in escape_dict:
                    temp_str += '\\' + s
                else:
                    temp_str += escape_dict[s]
                escaped = False
                continue

            match s:
                case '\\':
                    escaped = True

                case "'" | '"':
                    if str_open:
                        str_open = False
                    else:
                        str_open = True

                case ' ':
                    # check for the open string
                    if not str_open:
                        temp_args.append(temp_str)
                        temp_str = ''
                    else:
                        # add space to current string
                        temp_str += ' '

                case '\00':
                    temp_args.append(temp_str)

                case _:
                    temp_str += s

        if len(temp_args) < self.position_arguments:
            self.logger.debug('Too little arguments')
            return True, ArgumentParseError.TooLittleArguments

        if len(temp_args) > self.position_arguments + self.default_arguments:
            self.logger.debug('Too much arguments')
            return True, ArgumentParseError.TooMuchArguments

        for arg, targ in zip(self.arguments, temp_args):
            error, result = arg.typecast(targ)

            if error:
                self.logger.debug('can\'t cast the argument')
                log_exception(self.logger, result)
                return True, ArgumentParseError.IncorrectType

            setattr(output_args, arg.arg_name, result)
            
        return False, output_args

        #  self.logger.debug('Currently ArgumentParser.parse() is unavailable, return list back')
        #  return args[1:]
