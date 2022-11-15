import os
import logging
import time
import sys
import tomllib
from getpass import getpass
from telethon import TelegramClient, events
from .namespace import Namespace
from .translations import Translator
from . import pluginapi


class Instance:
    """Instance object of EasyTl userbot for Telegram

    :param api_id: API_ID from my.telegram.org -> Apps for telethon
    :type api_id: int
    :param api_hash: API_HASH from my.telegram.org -> Apps for telethon
    :type api_hash: str
    :param owner_id: Owner of EasyTl
    :type owner_id: int
    :param plugins_dir: Path to the directory with plugins
    :type plugins_dir: str
    :param cache_dir: Path to the directory with cache
    :type cache_dir: str
    :param config_dir: Path to the configuration directory
    :type config_dir: str
    :param logs_dir: Directory with the logs
    :type logs_dir: str
    :param translator: The translator object
    :type translator: Translator
    :param instance_name: Name of the instance
    :type instance_name: str

    :ivar prefixes: List with the EasyTl prefixes, by the default is "easy"
    :type prefixes: list[str]
    :ivar platform: The platform from the configuration directory
    :type platform: str
    :ivar client: Telethon TelegramClient instance
    :type client: TelegramClient
    :ivar namespace: Instance of the Namespace
    :type namespace: Namespace
    :ivar plugins: List with the plugins (Instance of PluginsList)
    :type plugins: pluginapi.PluginsList
    :ivar instance_name: Name of the instance
    :type instance_name: str
    :ivar logger: An Logger object
    :type logger: logging.Logger
    :ivar stdout_handler: An stream handler for the console output
    :type stdout_handler: logging.StreamHandler
    """

    def __init__(self, api_id: int, api_hash: str, owner_id: int, plugins_dir: str = os.path.join('.', 'plugins'),
                 cache_dir: str = os.path.join('.', 'cache'), config_dir: str = os.path.join('.', 'config'),
                 logs_dir: str = os.path.join('.', 'logs'), translator: Translator = Translator(lang='en'),
                 instance_name: str = 'Instance0'):

        self.api_id, self.api_hash, self.owner_id, self.plugins_dir, self.cache_dir, \
            = api_id, api_hash, owner_id, plugins_dir, cache_dir
        self.config_dir, self.logs_dir, self.translator, self.instance_name \
            = config_dir, logs_dir, translator, instance_name

        self.client = None
        self.logger = None
        self.stdout_handler = None

        self.prefixes = ['easy']
        self.platform = self.get_platform()
        self.namespace = Namespace({'cache_dir': self.cache_dir,
                                    'instance': self,
                                    'pluginapi': pluginapi,
                                    'translator': self.translator,
                                    'commands': {},
                                    'pcommands': {},
                                    'notify_stack': []})
        self.plugins = pluginapi.PluginsList(plugins_dir=self.plugins_dir, namespace=self.namespace)

        self.namespace.plugins = self.plugins

    def initialize(self):
        """Initializes the working environment for userbot"""

        self.logger.debug('Creating instance of TelegramClient in instance.client')

        # init telethon's TelegramClient
        self.client = TelegramClient('EasyTl', self.api_id, self.api_hash)
        self.namespace.client = self.client
        self.client.add_event_handler(self.messages_handler, events.NewMessage)

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
        self.plugins.activate_plugins_list(plugins_dict)

    def initialize_logging(self, log_level: int):
        """Initializes instance.Logger object

        :param log_level: Log level of logger (logging.INFO, logging.DEBUG and etc...)
        :type log_level: int
        """

        s_format = '%(name)s | %(asctime)s | [%(levelname)s] : %(message)s'
        formatter = logging.Formatter(s_format)

        logging.basicConfig(
            format=s_format, datefmt='%H:%M:%S',
            filename=os.path.join(self.logs_dir,
                                  self.instance_name +
                                  f'-{time.strftime("%Y-%m-%d_%H-%M", time.localtime())}-log.txt'),
            level=log_level
        )

        # init instance logger
        self.logger = logging.Logger('EasyTl')
        self.logger.setLevel(log_level)

        # init a stream handler for the console output
        self.stdout_handler = logging.StreamHandler(sys.stdout)
        self.stdout_handler.setLevel(log_level)
        self.stdout_handler.setFormatter(formatter)
        self.logger.addHandler(self.stdout_handler)

    def partial_run(self):
        """Only starts the telegram client"""

        self.logger.info('Telegram client run partial')
        self.client.start()

    def run(self):
        """Run the telegram client until disconnected"""

        self.logger.info('Run Telegram client')

        # run telethon TelegramClient
        self.client.start()
        self.client.run_until_disconnected()

    async def command_handler(self, length: int, cmd: list, event):
        """(System method) executing command

        :param length: Length of "cmd" list
        :type length: int
        :param cmd: The command, split by space list
        :type cmd: list
        :param event: Telethon's event variable
        """

        self.logger.debug(f'command_handler, LENGTH: {length} CMD: {cmd}')

        # check if the command is exists
        if length < 1 or cmd[0] not in self.namespace.commands:
            self.logger.debug(f'Command {cmd[0]} not found in instance.namespace.commands')
            return

        # check if the notify stack have some messages
        if len(self.namespace.notify_stack) > 0:
            for m in self.namespace.notify_stack:
                self.logger.debug('Send message from notify stack')
                await self.send(event, self.f_notify(m))  # send the message to a chat
                self.namespace.notify_stack.remove(m)  # remove the message from the notify stack

        self.logger.debug('Call the command with permissions')
        await self.namespace.call_w_permissions(self.namespace.commands[cmd[0]], event, cmd[1:])

    async def messages_handler(self, event):
        """(System method) handles the message from Telegram

        :param event: Telethon's event variable
        """

        # split message by space and check if message isn't empty
        msg_split = event.message.message.split(' ')
        if (l := len(msg_split)) == 0:
            return

        # check if the message is had some prefixes
        if msg_split[0] in self.prefixes:
            self.logger.debug(f'A message with the command has been detected, MSG_SPLIT: {msg_split}')
            await self.command_handler(l - 1, msg_split[1:], event)

    def get_platform(self) -> str:
        """Returns the build platform value (reads the "_platform" file in the config directory)

        :returns: Platform (windows or linux or android)
        :rtype: str
        """

        with open(os.path.join(self.config_dir, '_platform')) as f:
            return f.read()

    def get_version(self) -> str:
        """Returns the build version value (reads the "_version" file in the config directory)

        :returns: Version (current numeric version of EasyTl)
        :rtype: str
        """

        with open(os.path.join(self.config_dir, 'version.toml'), 'rb') as f:
            return tomllib.load(f)

    ####

    @staticmethod
    def f_notify(message: str) -> str:
        """Formats the message as notify

        :param message: A message to format
        :type message: str

        :returns: Formatted message
        :rtype: str
        """

        return '🔔  ' + message

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
        Shorthand for instance.send(event, instance.f_success(message))

        :param event: Telethon's event variable
        :param message: Message that will be formatted as success and sent
        :type message: str
        """

        await self.send(event, self.f_success(message))

    async def send_unsuccess(self, event, message: str):
        """Send message to current chat, formatted as unsuccess.
        Shorthand for instance.send(event, instance.f_success(message))

        :param event: Telethon's event variable
        :param message: Message that will be formatted as unsuccess and sent
        :type message: str
        """

        await self.send(event, self.f_unsuccess(message))
