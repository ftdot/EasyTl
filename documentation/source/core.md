# EasyTl documentation

## source.core
`source/core.py` is a core file with all main functional. At now is released only `Instance` class.

File: [src/source/core.py](../../src/source/core.py)

#### Instance `core.Instance`
```python
class Instance()
```
`Instance` class is providing an instance of EasyTl userbot. This class is main for all.

Example of usage:
```python
import logging
import os
import sys

from source.core import Instance
from source.translations import Translator

# settings
API_ID    = -1
API_HASH  = ''

MY_ID     = -1
lang      = 'en'

# advanced settings

OTHER_OWNERS = []

instance_name               = 'Main Instance'
enable_plugins_auto_update  = True  # enable the plugins auto-update feature?

install_dir  = os.getcwd()

plugins_dir  = os.path.join(install_dir, 'plugins')
cache_dir    = os.path.join(install_dir, 'cache')
lang_dir     = os.path.join(install_dir, 'translations')
logs_dir     = os.path.join(install_dir, 'logs')

win_ffmpeg_dir   = os.path.join(install_dir, 'ffmpeg', 'ffmpeg-master-latest-win64-gpl-shared')

log_level          = logging.DEBUG
console_log_level  = logging.INFO  # Set this to the logging.DEBUG if you want to see all the debug information

####

if __name__ == '__main__':
    main_instance = Instance(instance_name,
                             API_ID, API_HASH, [MY_ID, ] + OTHER_OWNERS,
                             'config.toml', Translator(lang_dir, lang),
                             install_dir, plugins_dir, cache_dir, logs_dir)
    main_instance.initialize_logging(True, log_level, console_log_level)

    main_instance.namespace.enable_plugins_auto_update  = enable_plugins_auto_update
    main_instance.namespace.ffmpeg_dir                  = win_ffmpeg_dir
    main_instance.namespace.instance_file               = os.path.abspath(__file__)

    main_instance.initialize()

    if len(sys.argv) == 2:
        if sys.argv[1] == 'restart':  # check if EasyTl started from the restart command
            # add notify about the restart

            main_instance.logger.debug('Add notify about a restart of the userbot')

            main_instance.namespace.notify_stack.append(
                main_instance.f_success(
                    main_instance.namespace.translations['core']['command.restart']['restarted_notify']
                )
            )

    main_instance.run()

```

#### Parameters + variables:

##### Instance.instance\_name `str`
Name of the instance.

##### Instance.api\_id `int`
API ID value for the telethon. You can get it there: [my.telegram.org](https://my.telegram.org) -> Apps

##### Instance.api\_hash `str`
API HASH value for the telethon. You can get it there: [my.telegram.org](https://my.telegram.org) -> Apps

##### Instance.owner\_id `int`
ID of the owner of the instance. You can get it from the Telegram bot [@myidbot](https://t.me/myidbot)

##### Instance.config_file `str`
Path to the file with TOML config of the instance.
Config is static, required values for work the EasyTl

##### Instance.translator `source.translator.Translator`
The instance of `Translator`.
By default: `Translator(lang='en')`

##### Instance.install\_dir `str`
Path to the directory there installed a EasyTl Instance.
By default: `'.'`

##### Instance.plugins\_dir `str`
Path to the directory there installed the plugins for the Instance.
By default: `os.path.join('.', 'plugins')`

##### Instance.cache\_dir `str`
Path to the directory there will be saved cache of the Instance.
By default: `os.path.join('.', 'cache')`

##### Instance.logs\_dir `str`
Path to the directory where save the logs.
By default: `os.path.join('.', 'plugins')`

#### Variables of the `Instance`:

##### Instance.prefixes `list[str]`
List with the prefixes of userbot.
By default: `['easy']`

##### Instance.client `telethon.TelegramClient`
Instance of the TelegramClient

##### Instance.namespace `source.namespace.Namespace`
Instance of the Namespace.
By default is have there values:
- `instance` (`source.core.Instance`) - link to the current instance
- `pluginapi` (`source.pluginapi`) - link to the pluginapi module
- `Namespace` (`source.namespace.Namespace`) - link to the Namespace class
- `Translator` (`source.namespace.Translator`) - link to the Namespace class
- `translator` (`source.translations.Translator`) - link to translator of current instance (`Instance.translator`)
- `commands` (`dict[str, function]`) - dict with the registered commands
- `pcommands` (`dict[str, list[str]]`) - dict with the commands(functions) names and permissions for it
- `notify_stack` (`list[str]`) - list with the notifies. It was send to the Telegram chat at first command

##### Instance.plugins `source.pluginapi.PluginsList`
Instance of `PluginsList`. By the way is a list with the plugins

##### Instance.logger `logging.Logger`
An `logging.Logger` instance

##### Instance.stdout\_handler `logging.StreamHandler`
An `logging.StreamHandler` instance for logging into the console. Is a handler for `sys.stdout`

#### Methods of the `Instance`:

##### Instance.initialize()
Initializes the working environment for userbot. Takes no argument (only `self`)

##### Instance.initialize\_logging()
Initializes instance.Logger object. Takes no argument (only `self`)

##### Instance.partialy\_run()
DELETED in v1.4.0

~~Run only `Instance.client`, without the call of `Instance.client.run_until_disconnected()`. Takes no argument (only `self`)~~

##### Instance.run()
Run `Instance.client` until disconnected from the Telegram. Takes no argument (only `self`)

##### async Instance.command\_handler()
(System method) Executes command. Arguments:
- `self`
- `length` (`int`) - Length of the splitted (by space) list
- `args` (`list`) - List with the command arguments
- `event` (`telethon.events.newmessage.NewMessage.Event`) - Telethon's event of the NewMessage

##### async Instance.message\_handler()
(System method) Handles the messages from the Telegram. Arguments:
- `self`
- `event` (`telethon.events.newmessage.NewMessage.Event`) - Telethon's event of the NewMessage

#### Getters for the config values:

##### Instance.get\_platform() -> `str`
DELETED IN v1.4.0. Use `Instance.config['platform']` instead of.

~~Reads and return a `\_platform` file value from the directory with configs (`Instance.config\_dir`). Takes no argument (only `self`)~~

##### Instance.get\_version() -> `dict`
DELETED IN v1.4.0. Use `Instance.config['version']` instead of.

~~Reads, parses TOML to dict and return a `version.toml` file value from the directory with configs (`Instance.config_dir`). Takes no argument (only `self`)~~

##### Instance.log_plugins_to_stdout() -> `bool`
DELETED IN v1.4.0. Use `Instance.config['log_plugins_to_stdout']` instead of.

~~Reads, parse from TOML to dict and return a `version.toml` file value from the directory with configs (`Instance.config\_dir`). Takes no argument (only `self`)~~

#### Static methods, formatters:
Methods there decorated with `@staticmethod`!

##### Instance.f\_notify() -> `str`
Formats a message argument as `🔔  (message)`. Arguments:
- `message` (`str`) - Message to be formatted

##### Instance.f\_warning() -> `str`
Formats a message argument as `EasyTl ⚠️ (message)`. Arguments:
- `message` (`str`) - Message to be formatted

##### Instance.f\_success() -> `str`
Formats a message argument as `EasyTl ✅ (message)`. Arguments:
- `message` (`str`) - Message to be formatted

##### Instance.f\_unsuccess() -> `str`
Formats a message argument as `EasyTl ❌ (message)`. Arguments:
- `message` (`str`) - Message to be formatted

#### Wrappers to send the text:

##### async Instance.send()
Send message to current chat. Shorthand for client.send_message(event.chat_id, ...). Arguments:
- `self`
- `event` (`telethon.events.newmessage.NewMessage.Event`)
- `message` (`str`) - Message to be send

##### async Instance.send\_success()
Send message to current chat, formatted as success. Shorthand for Instance.send(event, Instance.f_success(message)). Arguments:
- `self`
- `event` (`telethon.events.newmessage.NewMessage.Event`)
- `message` (`str`) - Message to be formatted and sent

##### async Instance.send\_unsuccess()
Send message to current chat, formatted as success. Shorthand for Instance.send(event, Instance.f_unsuccess(message)). Arguments:
- `self`
- `event` (`telethon.events.newmessage.NewMessage.Event`)
- `message` (`str`) - Message to be formatted and sent

##### async Instance.send\_notify()
Send message to current chat, formatted as success. Shorthand for Instance.send(event, Instance.f_notify(message)). Arguments:
- `self`
- `event` (`telethon.events.newmessage.NewMessage.Event`)
- `message` (`str`) - Message to be formatted and sent

##### async Instance.send\_warning()
Send message to current chat, formatted as success. Shorthand for Instance.send(event, Instance.f_warning(message)). Arguments:
- `self`
- `event` (`telethon.events.newmessage.NewMessage.Event`)
- `message` (`str`) - Message to be formatted and sent

#### Wrappers to get translated credentials:

##### Instance.\_t\_get\_code() -> `str`
Gets input for the code, but get the translation from `core.instance.telegram_get_code`

##### Instance.\_t\_get\_phone() -> `str`
Gets input for the phone, but get the translation from `core.instance.telegram_get_number`

##### Instance.\_t\_get\_password() -> `str`
Gets input for the password, but get the translation from `core.instance.telegram_get_code`