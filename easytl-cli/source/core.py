import os
import logging
import time
import sys
import tomllib
from getpass import getpass
from telethon import TelegramClient, events
from .namespace import Namespace
from .translator import Translator
from .argument_parser import ArgumentParser
from . import pluginapi


class Instance:
    """Instance object of EasyTl userbot for Telegram

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

    :ivar prefixes: List with the EasyTl prefixes, by the default is "easy"
    :type prefixes: list[str]
    :ivar client: Telethon TelegramClient instance
    :type client: TelegramClient
    :ivar namespace: Instance of the Namespace
    :type namespace: Namespace
    :ivar plugins: List with the plugins (Instance of PluginsList)
    :type plugins: pluginapi.PluginsList
    :ivar logger: An Logger object
    :type logger: logging.Logger
    :ivar stdout_handler: An stream handler for the console output
    :type stdout_handler: logging.StreamHandler
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

        self.api_id, self.api_hash, self.owner_ids, \
            = api_id, api_hash, owner_ids
        self.config_file, self.translator, self.instance_name \
            = config_file, translator, instance_name
        self.install_dir, self.plugins_dir, self.cache_dir, self.logs_dir \
            = install_dir, plugins_dir, cache_dir, logs_dir

        self.client = None
        self.config = None
        self.logger = None
        self.stdout_handler = None

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

        self.namespace.plugins = pluginapi.PluginsList(plugins_dir=self.plugins_dir, namespace=self.namespace)

    def initialize(self):
        """Initializes the working environment for userbot"""

        self.logger.debug('Creating instance of TelegramClient in instance.client')

        # init telethon's TelegramClient
        self.client = TelegramClient('EasyTl', self.api_id, self.api_hash)
        self.client.add_event_handler(self.messages_handler, events.NewMessage)
        self.namespace.client = self.client

        self.logger.debug('Loading config for the instance')

        with open(self.config_file, 'rb') as f:
            self.config = tomllib.load(f)

        self.logger.debug('Checking the config')
        self.check_config()

        self.logger.debug('Loading translator')

        # init the translator
        self.namespace.translator.namespace = self.namespace
        self.namespace.translator.load_languages()

        self.logger.debug('Loading plugins list')

        # load the plugins
        plugins_list = [pluginapi.Plugin(os.path.basename(f)[:-10], os.path.join(self.plugins_dir, f))
                            for f in
                                [f for f in os.listdir(self.plugins_dir) if f.endswith('.plugin.py')]
                        ]
        plugins_dict = {p.plugin_name: p for p in plugins_list}

        self.logger.info('Activating plugins')

        # activate all plugins
        self.namespace.plugins.activate_plugins_list(plugins_dict)

    def initialize_logging(self, log_level: int, console_log_level: int):
        """Initializes instance.Logger object

        :param log_level: Log level of logger (logging.INFO, logging.DEBUG and etc...)
        :type log_level: int
        :param console_log_level: Log level of console logging (logging.INFO, logging.DEBUG and etc...)
        :type console_log_level: int
        """

        s_format = '%(name)s | %(asctime)s | [%(levelname)s] : %(message)s'
        formatter = logging.Formatter(s_format)

        logging.basicConfig(
            format=s_format, datefmt='%H:%M:%S',
            filename=os.path.join(self.logs_dir,
                                  f'{time.strftime("%Y-%m-%d_%H-%M", time.localtime())}-log.txt'),
            level=log_level
        )

        # init a stream handler for the file
        file_handler = logging.FileHandler(
            os.path.join(self.logs_dir,
                         self.instance_name +
                         f'-{time.strftime("%Y-%m-%d_%H-%M", time.localtime())}-log.txt')
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)

        # init instance logger
        self.logger = logging.Logger('EasyTl Instance')
        self.logger.setLevel(log_level)
        self.logger.addHandler(file_handler)

        # init a stream handler for the console output
        self.stdout_handler = logging.StreamHandler(sys.stdout)
        self.stdout_handler.setLevel(console_log_level)
        self.stdout_handler.setFormatter(formatter)

        self.logger.addHandler(self.stdout_handler)

    def run(self):
        """Run the telegram client until disconnected"""

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

        self.client.run_until_disconnected()

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
        # because ArgumentParser is only preview in the v1.4.0 - it always return list without prefix
        # see v1.4.0 release (notes)
        if isinstance(command_func.ap, ArgumentParser):
            p_args = command_func.ap.parse(args)
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
