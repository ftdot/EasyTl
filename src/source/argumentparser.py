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

# number of messages to iter when reply-to functional is used
RT_ITER_NUM = 50


class ArgumentParseError(Enum):
    TooManyArguments = auto()
    TooLittleArguments = auto()
    IncorrectType = auto()
    IncorrectSubcommand = auto()
    ReplyToRequired = auto()
    CantFindOriginalMessage = auto()


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


class ListCast_(ArgTypeCast):
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

    def typecast(self, string: str) -> list[Any]:
        """Type-cast string to the list

        :param string: String to be type-casted
        :type string: str

        :return: Type-casted list object
        :rtype: list
        """

        return [self.values_type.typecast(v) for v in string.split(self.splitter)]


class DictCast_(ArgTypeCast):
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

    def __init__(self,
                 true_list: list[str] | None = None,
                 false_list: list[str] | None = None,
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
    BoolCast = BoolCast()

    @staticmethod
    def setup_bool_cast_translations(true_list: list[str], false_list: list[str]):
        """Set up the BoolCast type-cast translations

        :param true_list: List with the true string variants
        :type true_list: list[str]
        :param false_list: List with the false string variants
        :type false_list: list[str]
        """

        Cast.BoolCast = BoolCast(true_list, false_list)


class ListCast:
    ListStrCast = ListCast_()
    ListIntCast = ListCast_(values_type=Cast.IntCast)
    ListFloatCast = ListCast_(values_type=Cast.FloatCast)
    ListBoolCast = ListCast_(values_type=Cast.BoolCast)


class DictCast:
    DictStrStrCast = DictCast_()
    DictStrIntCast = DictCast_(values_type=Cast.IntCast)
    DictStrFloatCast = DictCast_(values_type=Cast.FloatCast)
    DictStrBoolCast = DictCast_(values_type=Cast.BoolCast)

    DictIntStrCast = DictCast_(key_type=Cast.IntCast)
    DictIntIntCast = DictCast_(key_type=Cast.IntCast, values_type=Cast.IntCast)
    DictIntFloatCast = DictCast_(key_type=Cast.IntCast, values_type=Cast.FloatCast)
    DictIntBoolCast = DictCast_(key_type=Cast.IntCast, values_type=Cast.BoolCast)


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
            return False, self.arg_type.typecast(input_arg) if input_arg != '' else self.default
        except Exception as e:
            return True, e


class ReplyToArgument(Argument):
    """Argument for the Reply-To functional"""
    pass


# cache of the ArgumentParser
_CACHED = {}


class ArgumentParser:
    """Helps to manage the arguments
    
    :ivar parent_plugin: Parent plugin of this parser
    :type parent_plugin: Plugin
    :ivar arguments: List with the arguments
    :type arguments: list[Argument]
    :ivar allow_caching: Use the caching when it parses the arguments
    :type allow_caching: bool
    :ivar logger: Logger of the argument parser
    :type logger: logging.Logger
    :ivar position_arguments: Number of the position arguments
    :type position_arguments: int
    :ivar default_arguments: Number of the default arguments
    :type default_arguments: int
    """

    def __init__(self,
                 parent_plugin,
                 arguments: list[Argument],
                 allow_caching: bool = True,
                 enable_escaping: bool = False,
                 subcommands: bool = False,
                 main_command_aliases: str | list[str] | None = None
                 ):
        """
        :param parent_plugin: Parent plugin of this parser
        :type parent_plugin: Plugin
        :param arguments: List with the arguments
        :type arguments: list[Argument]
        :param allow_caching: Use the caching when it parses the arguments
        :type allow_caching: bool
        :param enable_escaping: Enable the escaping by "\" character
        :type enable_escaping: bool
        :param subcommands: Enable the subcommands feature
        :type subcommands: bool
        :param main_command_aliases: Name of the main commands (requires "subcommands")
        :type main_command_aliases: str | list[str] | None = None
        """

        self.parent_plugin = parent_plugin
        self.arguments = arguments
        self.allow_caching = allow_caching
        self.enable_escaping = enable_escaping
        self.subcommands = subcommands

        self.logger = logging.getLogger('EasyTl : ArgumentParser')

        self.logger.debug('Initializing the values')
        self.position_arguments = 0
        self.default_arguments = 0

        for arg in self.arguments:
            if arg.default:
                self.default_arguments += 1
                continue

            self.position_arguments += 1

        self.subcommands_dict = {}

        if self.subcommands:
            # create empty command by the plugin decorator
            self.parent_plugin.command(main_command_aliases, ap=self)(self.parent_plugin.async_empty)

        # check for the reply-to argument
        if len(self.arguments) > 0 and isinstance(self.arguments[0], ReplyToArgument):
            if self.arguments[0].default is None:
                self.position_arguments -= 1

    def _cached_check(self, string: str) -> list[str]:
        """Checker for the caching

        :param string: Result work or cached string
        :type string: str

        :return: Executed cached result or already cached result of the parse_string() method
        :rtype: list[str]
        """

        if not self.allow_caching:
            return self.parse_string(string)

        # get hash of the string
        str_hash = hash(string)

        if str_hash not in _CACHED:
            _CACHED[str_hash] = self.parse_string(string)

        return _CACHED[str_hash]

    ####

    def parse_string(self, string: str) -> list[str]:
        """Parses the string to the list with the arguments

        :param string: String to parse
        :type string: str
        
        :return: List with the parsed arguments
        :rtype: list[str]
        """

        # initialize the variables to first parse stage
        str_open = False
        str_open_char = None
        temp_str = ''
        temp_args = []
        escaped = False

        # first parse stage (strings with spaces, escaping)
        for s in string:

            if escaped:
                if s not in escape_dict:
                    # do not escape the character
                    temp_str += '\\' + s
                else:
                    # escape the character to other character in escape dict
                    temp_str += escape_dict[s]

                escaped = False
                continue

            match s:
                case '\\':
                    # check if escaping is enabled
                    if not self.enable_escaping:
                        continue

                    escaped = True

                case "'" | '"':
                    # check if characters is different
                    if str_open_char is not None and str_open_char != s:
                        temp_str += s
                        continue

                    # check for the opened string
                    if str_open:
                        str_open = False
                        str_open_char = None
                    else:
                        str_open = True
                        str_open_char = s

                case ' ':
                    # check for the open string
                    if not str_open:
                        temp_args.append(temp_str)
                        temp_str = ''
                    else:
                        # add space to current string
                        temp_str += ' '

                case '\00':
                    if temp_str != '':
                        temp_args.append(temp_str)

                case _:
                    temp_str += s

        return temp_args

    async def parse(self, args: list[str], event, command_func) -> (bool, Namespace | ArgumentParseError):
        """Parses the default EasyTl arguments system to new & execute the command

        :param args: List with the arguments
        :type args: list[str]
        :param event: Telethon event
        :param command_func: Command function
        :type command_func: (Any, Namespace) -> None

        :return: Namespace with the parsed arguments
        :rtype: (bool, Namespace | ArgumentParseError)
        """

        self.logger.debug('ArgumentParser called with arguments: ' + ', '.join(args))

        # check for the subcommands
        if self.subcommands:
            self.logger.debug('Command with subcommands has called')

            # check for the arguments length
            if len(args) < 2:
                self.logger.debug('Too little arguments')
                return ArgumentParseError.TooLittleArguments

            # check for the subcommand
            if args[2] in self.subcommands_dict:
                self.logger.debug('Call the subcommand function')
                func = self.subcommands_dict[args[2]]  # get function

                # check for the ArgumentParser is using in command
                if func.ap is not None:
                    return await func.ap.parse([args[0]] + args[2:], event, func)

                self.logger.info(f'Function {func.__name__} (command: {args[2]}) doesn\'t have ArgumentParser!')
                return None
            else:
                return ArgumentParseError.IncorrectSubcommand

        # initialize the variables
        output_args = Namespace()
        output_args.PREFIX = args[0]
        output_args.CMD = args[1]
        temp_args = []

        if len(args) > 2:
            input_str = ' '.join(args[2:]) + '\00'

            # parse the stringuity
            temp_args = self._cached_check(input_str)

        # check for the reply-to argument
        if len(self.arguments) > 0 and isinstance(self.arguments[0], ReplyToArgument):
            arg = self.arguments[0]

            # check if message has reply-to
            if event.reply_to:
                # find reply-to message
                msg = [msg async for msg in self.parent_plugin.namespace.instance.client.iter_messages(event.chat_id, RT_ITER_NUM)
                       if msg.id == event.reply_to.reply_to_msg_id]
                if len(msg) == 0:
                    return ArgumentParseError.CantFindOriginalMessage
                msg = msg[0]

                # type-cast the argument
                error, result = arg.typecast(msg.message)

                # check for the error
                if error:
                    self.logger.debug('can\'t cast the argument')
                    log_exception(self.logger, result)

                    return ArgumentParseError.IncorrectType

                # set up the type-casted reply-to message
                setattr(output_args, arg.arg_name, result)
                setattr(output_args, 'REPLY_TO_MESSAGE', msg)
            else:
                if arg.default is None:
                    return ArgumentParseError.ReplyToRequired

        # compare the positional arguments
        if len(temp_args) < self.position_arguments:
            self.logger.debug('Too little arguments')
            return ArgumentParseError.TooLittleArguments

        # compare the arguments sum length
        if len(temp_args) > self.position_arguments + self.default_arguments:
            self.logger.debug('Too much arguments')
            return ArgumentParseError.TooManyArguments

        # initialize the default arguments
        for arg in self.arguments:
            if arg.default:
                setattr(output_args, arg.arg_name, arg.default)

        # type-cast & define the arguments
        for arg, targ in zip(self.arguments, temp_args):
            # type-cast the argument
            error, result = arg.typecast(targ)

            # check for the error
            if error:
                self.logger.debug('can\'t cast the argument')
                log_exception(self.logger, result)

                return ArgumentParseError.IncorrectType

            # define variable
            setattr(output_args, arg.arg_name, result)

        # call the command
        await self.parent_plugin.namespace.call_w_permissions(command_func, event, output_args)

        return None

    ####

    def subcommand(self, aliases: str | list | None = None, ap=None, static_pname: str | None = None):
        """Decorator, that helps register the new subcommand.
           This is redirects to the `parent_plugin.command` decorator

        :param aliases: Aliases to the command
        :type aliases: str | list | None
        :param ap: Argument parser
        :type ap: ArgumentParser | None
        :param static_pname: Static name in the namespace.pcommands dict
        :type static_pname: str | None

        :returns: func with the changed attributes
        """

        def deco(func):
            nonlocal aliases

            # register command by the plugins decorator
            func = self.parent_plugin.command(aliases, ap, static_pname)(func)

            # register aliases in the argument parser subcommands dict
            aliases = aliases if isinstance(aliases, list) else [aliases, ]
            for a in aliases:
                self.subcommands_dict[a] = func

            return func

        return deco
