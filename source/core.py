import os
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
    :param translator: The translator object
    :type translator: Translator

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
    """

    def __init__(self, api_id: int, api_hash: str, owner_id: int, plugins_dir: str = os.path.join('.', 'plugins'),
                 cache_dir: str = os.path.join('.', 'cache'), config_dir: str = os.path.join('.', 'config'),
                 translator: Translator = Translator(lang='en')):

        self.api_id, self.api_hash, self.owner_id, self.plugins_dir, self.cache_dir, self.config_dir, self.translator \
            = api_id, api_hash, owner_id, plugins_dir, cache_dir, config_dir, translator

        self.prefixes = ['easy']
        self.platform = self.get_platform()
        self.client = None
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

        # init telethon's TelegramClient
        self.client = TelegramClient('EasyTl', self.api_id, self.api_hash)
        self.namespace.client = self.client
        self.client.add_event_handler(self.messages_handler, events.NewMessage)

        # init the translator
        self.namespace.translator.namespace = self.namespace
        self.namespace.translator.load_language()

        # load the plugins
        plugins_list = [pluginapi.Plugin(os.path.basename(f)[:-10], os.path.join(self.plugins_dir, f))
                        for f in
                                [f for f in os.listdir(self.plugins_dir) if f.endswith('.plugin.py')]
                        ]
        plugins_dict = {p.plugin_name: p for p in plugins_list}

        # activate all plugins
        self.plugins.activate_plugins_list(plugins_dict)

    def run(self):
        """Run an instance"""

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

        # check if the command is exists
        if length < 1 or cmd[0] not in self.namespace.commands:
            return

        # check if the notify stack have some messages
        if len(self.namespace.notify_stack) > 0:
            for m in self.namespace.notify_stack:
                await self.send(event, self.f_notify(m))  # send the message to a chat
                self.namespace.notify_stack.remove(m)  # remove the message from the notify stack

        await self.namespace.call_w_permissions(self.namespace.commands[cmd[0]], event, cmd[1:], cmd[0])

    async def messages_handler(self, event):
        """(System method) handles the message from Telegram

        :param event: Telethon's event variable
        """

        # split message by space and check if message isn't empty
        msg_split = event.message.message.split(' ')
        if (l := len(msg_split)) == 0:
            return

        # check if the message is have some prefixes
        if msg_split[0] in self.prefixes:
            await self.command_handler(l-1, msg_split[1:], event)

    def get_platform(self) -> str:
        """Returns the build platform value (read the "_platform" file in the config directory)

        :returns: Platform (windows or linux or android)
        :rtype: str
        """

        with open(os.path.join(self.config_dir, '_platform')) as f:
            return f.read()

    ####

    @staticmethod
    def f_notify(message: str) -> str:
        """Formats the message as notify

        :param message: A message to format
        :type message: str

        :returns: Formatted message
        :rtype: str
        """

        return '🔔  '+message

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
