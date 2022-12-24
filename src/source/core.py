import os
import logging
import time
import sys
import tomlkit
from getpass import getpass
from telethon import TelegramClient, events
from .namespace import Namespace
from .translator import Translator
from .argumentparser import ArgumentParser, ArgumentParseError
from . import pluginapi


class Instance:
    """Instance object of EasyTl userbot for Telegram

    :ivar instance_name: Name of the instance
    :type instance_name: str
    :ivar api_id: API_ID from my.telegram.org -> Apps, for the telethon
    :type api_id: int
    :ivar api_hash: API_HASH from my.telegram.org -> Apps, for the telethon
    :type api_hash: str
    :ivar owner_ids: Owners of Instance
    :type owner_ids: list[int]
    :ivar config_file: Path to the file with TOML config of the instance
    :type config_file: str
    :ivar translator: The translator object
    :type translator: Translator
    :ivar install_dir: Path to the directory with the instance
    :type install_dir: str
    :ivar plugins_dir: Path to the directory with the plugins
    :type plugins_dir: str
    :ivar cache_dir: Path to the directory with the cache
    :type cache_dir: str
    :ivar logs_dir: Directory with the logs
    :type logs_dir: str
    :ivar logs_dir: Directory with the logs
    :type logs_dir: str
    :ivar prefixes: List with the EasyTl prefixes, by the default is "easy"
    :type prefixes: list[str]
    :ivar client: Telethon TelegramClient instance
    :type client: TelegramClient
    :ivar config: System configuration of the EasyTl-CLI
    :type config: dict[str, Any]
    :ivar namespace: Instance of the Namespace
    :type namespace: Namespace
    :ivar plugins: List with the plugins (Instance of PluginsList)
    :type plugins: pluginapi.PluginsList
    :ivar logger: An Logger object
    :type logger: logging.Logger
    :ivar addition_handlers: The addition handlers for the logging
    :type addition_handlers: list[logging.StreamHandler]
    """

    def __init__(self,
                 instance_name: str,
                 api_id: int,
                 api_hash: str,
                 owner_ids: list[int],
                 config_file: str,
                 translator: Translator = Translator(lang='en'),
                 install_dir: str = '.',
                 plugins_dir: str = os.path.join('.', 'plugins'),
                 cache_dir: str = os.path.join('.', 'cache'),
                 logs_dir: str = os.path.join('.', 'logs')
                 ):
        """
        :param instance_name: Name of the instance
        :type instance_name: str
        :param api_id: API_ID from my.telegram.org -> Apps, for the telethon
        :type api_id: int
        :param api_hash: API_HASH from my.telegram.org -> Apps, for the telethon
        :type api_hash: str
        :param owner_ids: Owners of Instance
        :type owner_ids: list[int]
        :param config_file: Path to the file with TOML config of the instance
        :type config_file: str
        :param translator: The translator object
        :type translator: Translator
        :param install_dir: Path to the directory with the instance
        :type install_dir: str
        :param plugins_dir: Path to the directory with the plugins
        :type plugins_dir: str
        :param cache_dir: Path to the directory with the cache
        :type cache_dir: str
        :param logs_dir: Directory with the logs
        :type logs_dir: str
        :param logs_dir: Directory with the logs
        :type logs_dir: str
        """

        self.api_id, self.api_hash, self.owner_ids, \
            = api_id, api_hash, owner_ids
        self.config_file, self.translator, self.instance_name \
            = config_file, translator, instance_name
        self.install_dir, self.plugins_dir, self.cache_dir, self.logs_dir \
            = install_dir, plugins_dir, cache_dir, logs_dir

        self.client             = None
        self.config             = None
        self.logger             = None
        self.addition_handlers  = []

        self.prefixes = ['easy', ]

        # initialize working namespace
        self.namespace               = Namespace()
        self.namespace.instance      = self
        self.namespace.pluginapi     = pluginapi
        self.namespace.Namespace     = Namespace
        self.namespace.Translator    = Translator
        self.namespace.translator    = self.translator
        self.namespace.commands      = {}
        self.namespace.pcommands     = {}
        self.namespace.notify_stack  = []

        # load the plugins
        plugins_list = [pluginapi.Plugin(os.path.basename(f)[:-10], os.path.join(self.plugins_dir, f))
                        for f in
                        [f for f in os.listdir(self.plugins_dir) if f.endswith('.plugin.py')]
                        ]
        plugins_dict = {p.plugin_name: p for p in plugins_list}

        self.namespace.plugins = pluginapi.PluginsList(plugins_dict,
                                                       plugins_dir=self.plugins_dir,
                                                       namespace=self.namespace)

    def initialize(self):
        """Initializes the working environment for userbot"""

        self.logger.debug('Creating instance of TelegramClient in instance.client')

        # init telethon's TelegramClient
        self.client = TelegramClient('EasyTl-'+self.instance_name, self.api_id, self.api_hash)
        self.client.add_event_handler(self.messages_handler, events.NewMessage)
        self.namespace.client = self.client

        self.logger.debug('Loading config for the instance')

        with open(self.config_file, 'r') as f:
            self.config = tomlkit.load(f)

        self.logger.debug('Checking the config')
        self.check_config()

        self.logger.debug('Loading translator')

        # init the translator
        self.namespace.translator.namespace = self.namespace
        self.namespace.translator.load_languages()

        self.logger.debug('Loading plugins list')

        # activate the plugins
        self.logger.info('Activating plugins')

        self.namespace.plugins.activate_plugin_list()

    def initialize_logging(self,
                           auto_config: bool = False,
                           log_level: str | int = logging.DEBUG,
                           console_log_level: str | int = logging.INFO,
                           disable_telethon_loggers: bool = True,
                           disable_utils_logger: bool = False):
        """Initializes the logging system

        :param auto_config: Auto configure the logging
        :type auto_config: bool
        :param log_level: Log level of logger (logging.INFO, logging.DEBUG and etc...)
        :type log_level: int
        :param console_log_level: Log level of console logging (logging.INFO, logging.DEBUG and etc...) (DEFAULT: logging.INFO)
        :type console_log_level: int
        :param disable_telethon_loggers: Set the telethon loggers log level to logging.ERROR level
        :type disable_telethon_loggers: bool
        :param disable_utils_logger: Set the utils logger log level to logging.ERROR level
        :type disable_utils_logger: bool
        """

        if auto_config:
            s_format = '%(name)s | %(asctime)s | [%(levelname)s] : %(message)s'
            formatter = logging.Formatter(s_format)

            # init a stream handler for the console output
            stdout_handler = logging.StreamHandler(sys.stdout)
            stdout_handler.setFormatter(formatter)
            stdout_handler.setLevel(console_log_level)

            # init a stream handler for the file
            file_handler = logging.FileHandler(
                os.path.join(self.logs_dir, f'{time.strftime("%Y-%m-%d_%H-%M", time.localtime())}-log.txt'),
                'w',
                'utf8'
            )
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.DEBUG)

            # add handlers to the list with it
            self.addition_handlers.append(stdout_handler)
            self.addition_handlers.append(file_handler)

            # configure the logger
            logging.basicConfig(
                format=s_format, datefmt='%H:%M:%S',
                handlers=self.addition_handlers,
                level=log_level
            )

        if disable_telethon_loggers:
            logging.getLogger('telethon.extensions.messagepacker').setLevel(logging.ERROR)
            logging.getLogger('telethon.network.mtprotosender').setLevel(logging.ERROR)

        if disable_telethon_loggers:
            logging.getLogger('EasyTl : Utils').setLevel(logging.ERROR)

        # init instance logger
        self.logger = logging.getLogger('EasyTl : Instance')

        self.logger.info('Logging is initialized')

    def run(self, run_until_disconnected: bool = True):
        """Run the telegram client until disconnected

        :param run_until_disconnected: Call the telethon client method "run_until_disconnected()" (Default: True)
        :type run_until_disconnected: bool
        """

        self.logger.info('Run Telegram client')

        # run telethon TelegramClient
        self.client.start(
            phone=self._t_get_phone,
            password=self._t_get_password,
            code_callback=self._t_get_code
        )

        if self.config['version']['indev']:
            self.logger.info('Current version may be unstable, because this version in the development')
        if self.config['version']['beta']:
            self.logger.info('This is a beta version. If you have some problems with EasyTl, '
                             'inform about it there: https://github.com/ftdot/EasyTl/issues')
        
        if run_until_disconnected:
            self.client.run_until_disconnected()

    ####

    async def command_handler(self, length: int, args: list, event):
        """(System method) Executes the command

        :param length: Length of "cmd" list
        :type length: int
        :param args: The args, split by space list
        :type args: list
        :param event: Telethon's event variable
        """

        self.logger.debug(f'command_handler, LENGTH: {length} ARGS: {args}')

        # check if the command is exists
        if length < 1 or args[1] not in self.namespace.commands:
            self.logger.debug(f'Command {args[1]} not found in Instance.namespace.commands')
            return

        # check if the notify stack have some messages
        await self.check_notifies_stack(event)

        # get function for the command
        command_func = self.namespace.commands[args[1]]

        # parsing the arguments or use arguments list without prefix
        # WARNING! Raw arguments list without prefix will be deleted in 1.5.1 releases
        if isinstance(command_func.ap, ArgumentParser):
            error, result = await command_func.ap.parse(args)
            if error:
                match result:
                    case ArgumentParseError.TooLittleArguments:
                        await self.send_unsuccess(
                            event,
                            self.namespace.translations['core']['argumentparser']['too_little_arguments']
                        )

                    case ArgumentParseError.TooManyArguments:
                        await self.send_unsuccess(
                            event,
                            self.namespace.translations['core']['argumentparser']['too_much_arguments']
                        )

                    case ArgumentParseError.IncorrectType:
                        await self.send_unsuccess(
                            event,
                            self.namespace.translations['core']['argumentparser']['incorrect_type']
                        )
                return

            p_args = result

        else:
            p_args = args[1:]

        self.logger.debug('Call the command with permissions')
        await self.namespace.call_w_permissions(command_func, event, p_args)

    async def messages_handler(self, event):
        """(System method) Handles the messages from the Telegram

        :param event: Telethon's event variable
        """

        # split message by space and check if message isn't empty
        msg_split = event.message.message.split(' ')
        if (l := len(msg_split)) == 0:
            return

        # check if the message is had some prefixes
        if msg_split[0] in self.prefixes:
            self.logger.debug(f'A message with the command has been detected, MSG_SPLIT: {msg_split}')
            await self.command_handler(l - 1, msg_split, event)

    ####

    async def check_notifies_stack(self, event):
        """Do check for the notifies stack. If any, send to the current chat

        :param event: Telethon's event variable
        """

        if len(self.namespace.notify_stack) > 0:
            for m in self.namespace.notify_stack:
                self.logger.debug(f'Send message from notify stack: {m}')
                await self.send(event, self.f_notify(m))  # send the message to a chat

            self.namespace.notify_stack = []  # clear the notifies stack

    def check_config(self):
        """Checks for the config values"""

        if self.config['build_platform'] == '':
            self.config['build_platform'] = 'windows' if sys.platform == 'win32' else 'linux'

    ####

    @staticmethod
    def f_success(message: str) -> str:
        """Formats the message as success

        :param message: A message to format
        :type message: str

        :returns: Formatted message
        :rtype: str
        """

        return f'`EasyTl` ✅ {message}'

    @staticmethod
    def f_unsuccess(message: str) -> str:
        """Formats the message as unsuccess

        :param message: A message to format
        :type message: str

        :returns: Formatted message
        :rtype: str
        """

        return f'`EasyTl` ❌ {message}'

    @staticmethod
    def f_notify(message: str) -> str:
        """Formats the message as notify

        :param message: A message to format
        :type message: str

        :returns: Formatted message
        :rtype: str
        """

        return '`EasyTl` 🔔  ' + message

    @staticmethod
    def f_warning(message: str) -> str:
        """Formats the message as warning

        :param message: A message to format
        :type message: str

        :returns: Formatted message
        :rtype: str
        """

        return f'`EasyTl` ⚠️ {message}'

    async def send(self, event, message: str):
        """Send message to current chat.
        Shorthand for client.send_message(event.chat_id, ...)

        :param event: Telethon's event variable
        :param message: Message that will be sent
        :type message: str
        """

        self.logger.debug(f'Send message to the CHAT_ID: {event.chat_id} MESSAGE: {message}')
        await self.client.send_message(event.chat_id, message)

    async def send_success(self, event, message: str):
        """Send message to current chat, formatted as success.
        Shorthand for Instance.send(event, Instance.f_success(message))

        :param event: Telethon's event variable
        :param message: Message that will be formatted as success and sent
        :type message: str
        """

        await self.send(event, self.f_success(message))

    async def send_unsuccess(self, event, message: str):
        """Send message to current chat, formatted as unsuccess.
        Shorthand for Instance.send(event, Instance.f_unsuccess(message))

        :param event: Telethon's event variable
        :param message: Message that will be formatted as unsuccess and sent
        :type message: str
        """

        await self.send(event, self.f_unsuccess(message))

    async def send_notify(self, event, message: str):
        """Send message to current chat, formatted as notify.
        Shorthand for Instance.send(event, Instance.f_notify(message))

        :param event: Telethon's event variable
        :param message: Message that will be formatted as notify and sent
        :type message: str
        """

        await self.send(event, self.f_notify(message))

    async def send_warning(self, event, message: str):
        """Send message to current chat, formatted as warning.
        Shorthand for Instance.send(event, Instance.f_warning(message))

        :param event: Telethon's event variable
        :param message: Message that will be formatted as warning and sent
        :type message: str
        """

        await self.send(event, self.f_warning(message))

    ####

    async def _t_get_code(self) -> str:
        """(System method) This method is using for get input (from the user) to authorize to the telegram.
        But, this method is support translating

        :return: User entered code
        :rtype: str
        """

        return input(self.namespace.translations['core']['instance']['telegram_get_code'])

    def _t_get_phone(self) -> str:
        """(System method) This method is using for get input (from the user) to authorize to the telegram.
        But, this method is support translating

        :return: User entered phone number
        :rtype: str
        """

        return input(self.namespace.translations['core']['instance']['telegram_get_number'])

    def _t_get_password(self) -> str:
        """(System method) This method is using for get input (from the user) to authorize to the telegram.
        But, this method is support translating

        :return: User entered password
        :rtype: str
        """

        return input(self.namespace.translations['core']['instance']['telegram_get_password'])
