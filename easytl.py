
import os
from source.core import Instance
from source.translations import Translator

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

plugins_dir = os.path.join(os.getcwd(), 'plugins')
cache_dir = os.path.join(os.getcwd(), 'cache')
lang_dir = os.path.join(os.getcwd(), 'lang')
config_dir = os.path.join(os.getcwd(), 'config')

# do not change the code below. It may cause problems!
if __name__ == '__main__':
    main_instance = Instance(API_ID, API_HASH, MY_ID, plugins_dir, cache_dir, config_dir, Translator(lang_dir, lang))
    main_instance.initialize()
    main_instance.run()
