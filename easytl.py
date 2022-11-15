import logging
import os
import sys

from source.core import Instance
from source.translations import Translator

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

instance_name = 'Main Instance'

plugins_dir  = os.path.join(os.getcwd(), 'plugins')
cache_dir    = os.path.join(os.getcwd(), 'cache')
lang_dir     = os.path.join(os.getcwd(), 'lang')
config_dir   = os.path.join(os.getcwd(), 'config')
logs_dir     = os.path.join(os.getcwd(), 'logs')

log_level          = logging.DEBUG
console_log_level  = logging.INFO  # Set this to the logging.DEBUG if you want to see all the debug information

# test_creds contains settings for this instance to do the tests
if os.path.exists('test_creds.py'):
    from test_creds import *

# do not change the code below. It may cause problems!
if __name__ == '__main__':
    main_instance = Instance(API_ID, API_HASH, MY_ID,
                             plugins_dir, cache_dir, config_dir, logs_dir,
                             Translator(lang_dir, lang), instance_name)
    main_instance.initialize_logging(log_level)
    main_instance.initialize()

    main_instance.namespace.instance_file = os.path.abspath(__file__)

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
