import logging
import os
import sys

from source.core import Instance
from source.translator import Translator

# There is EasyTl usebot default instance

# How to get API_ID and API_HASH:
#    - Sign up for Telegram using any application.
#    - Log in to your Telegram core: https://my.telegram.org.
#    - Go to "API development tools" and fill out the form.
#    - You will get basic addresses as well as the api_id and api_hash parameters

# settings
API_ID    = -1
API_HASH  = ''

MY_ID     = -1               # ur id from @myidbot
lang      = 'en'             # language of userbot

# advanced settings

# List with the ids of other owners. It may be danger, because danger commands be also trusted to it!
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

# test_creds contains settings for this instance to do the tests
if os.path.exists('test_creds.py'):
    from test_creds import *

# do not change the code below. It may cause problems!
if __name__ == '__main__':
    main_instance = Instance(instance_name,
                             API_ID, API_HASH, [MY_ID, ] + OTHER_OWNERS,
                             'config.toml', Translator(lang_dir, lang),
                             install_dir, plugins_dir, cache_dir, logs_dir)
    main_instance.initialize_logging(log_level, console_log_level)

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
