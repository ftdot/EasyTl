<p align="center">
  <img src="https://github.com/ftdot/ftdot/raw/main/imgs/easytl_banner_nb.png" />
</p>

[![Latest tag](https://img.shields.io/github/v/tag/ftdot/EasyTl?label=LATEST%20TAG&style=for-the-badge)](https://github.com/ftdot/EasyTl/tags)
[![Issues](https://img.shields.io/github/issues/ftdot/EasyTl?style=for-the-badge)](https://github.com/ftdot/EasyTl/issues)
# EasyTl
This is a userbot for Telegram, that have very comfortable plugin API.
**EasyTl** is the recreated project **ftub**, named also as **tub**.

## Navigation
<a href="https://github.com/ftdot/EasyTl/README.md#usage">Usage</a>
- <a href="https://github.com/ftdot/EasyTl/README.md#clone-repository-to-the-local-directory">Clone repository to the local directory</a>
- <a href="https://github.com/ftdot/EasyTl/README.md#enter-to-the-directory">Enter to the directory</a>
- <a href="https://github.com/ftdot/EasyTl/README.md#set-up-api_id-api_hash-and-my_id-in-easytlpy">Set up API_ID, API_HASH and MY_ID in easytl.py</a>
- <a href="https://github.com/ftdot/EasyTl/README.md#run-this">Run this</a>

<a href="https://github.com/ftdot/EasyTl/README.md#why-you-shouldnt-use-the-userbot-now">Why you shouldn't use the userbot now?</a>

<a href="https://github.com/ftdot/EasyTl/README.md#what-is-planning-in-this-project">What is planning in this project?</a>

## Usage
Currently this version is alpha-test, this means that the project is unstable and haven't full documentation.
Report any bug if you found there - https://github.com/ftdot/EasyTl/issues

#### Clone repository to the local directory
    # git clone https://github.com/ftdot/easytl
#### Enter to the directory
    # cd easytl
#### Set up API_ID, API_HASH and MY_ID in easytl.py
Open a file ``easytl.py`` by any editor and change these lines:
```python
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
```

Fast guide:
* Go to page https://my.telegram.org/
* Authorize with telegram to this page
* Go to Apps tab
* Create app
* Copy a value "API ID", replace `` API_ID = -1`` to the ``API_ID = [Your API ID]``
* Copy a value "API HASH", replace `` API_HASH = ''`` to the ``API_ID = '[Your API HASH]'``
* Go to the telegram and write to the bot @myidbot
* Copy your id from the bot and write it to the ``MY_ID`` also as the API_ID (replace -1 with your id)

After that manipulations, you must get something that:
```python
# settings
API_ID    = 55555555
API_HASH  = 'aaaabbbbccccddddeeeeffffgggghhhh'

MY_ID     = 9999999999       # ur id from @myidbot
lang      = 'ua'             # language of userbot
```
You may also change value ``lang`` to your country code. Its change the interface language

By default there languages are available:
* ``en`` - English
* ``ru`` - Russian
* ``ua`` - Ukrainian

#### Run this
After you configured the userbot, run that.
For Linux:
    # python3 easytl.py
For Windows:
    # python easytl.py

For first run, the userbot will ask you for the credetinals (Number and code). This is required to authorize the userbot

## Why you shouldn't use the userbot now?
At the moment it is unstable and not have full documentation and functional, that required for normal work with this project.

You can see my plugins for EasyTl there: https://github.com/ftdot/easytl-plugins/

## What is planning in this project?
* Easy PluginAPI (already do, but it unstable)
* Easy utilities as: configs, translations, plugin auto-update (Translations and auto-update already do)
* Full, easy to read, documentation
* Easy to use, cool GUI
* Cross-platform (including Android)
