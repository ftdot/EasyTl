<p align="center">
  <img src="https://github.com/ftdot/ftdot/raw/main/imgs/easytl_banner_nb-new.png" />
</p>

[![Latest tag](https://img.shields.io/github/v/tag/ftdot/EasyTl?label=LATEST%20TAG&style=for-the-badge)](https://github.com/ftdot/EasyTl/tags)
[![Project telegram](https://badgen.net/badge/icon/telegram?icon=telegram&label=EASYTL&style=for-the-badge&scale=1.4)](https://t.me/easytl)
[![Issues](https://img.shields.io/github/issues/ftdot/EasyTl?style=for-the-badge)](https://github.com/ftdot/EasyTl/issues)

# EasyTl
This is a userbot for Telegram, that have very comfortable plugin API, that allows for the developers easily create the plugins. 
Plugins extends the functional of the Telegram, adding to it the user-side commands, with that u can do everything u want.

**Our official telegram channel:** [@easytl](https://t.me/easytl)

#### EasyTl is the recreated project _ftub_, named also as _tub_.

## 📘 Navigation
📖 [Usage](#usage)
- [Clone repository to the local directory](#clone-repository-to-the-local-directory)
- [Enter to the directory](#enter-to-the-directory)
- [Setup](#setup)
- - [For the Linux](#for-the-linux)
- - [For the Windows](#for-the-windows)
- [(Optional) Set up the FFMPEG (Need for STTLib plugin)](#optional-set-up-the-ffmpeg-need-for-sttlib-plugin)
- - [For the Linux (Debian)](#for-the-linux-debian)
- - [For the Windows](#for-the-windows-1)
- [Set up API_ID, API_HASH and MY_ID in easytl.py](#set-up-api_id-api_hash-and-my_id-in-easytlpy)
- - [Fast guide](#fast-guide)
- [Run it](#run-it)

❓ <a href="https://github.com/ftdot/EasyTl/README.md#why-you-shouldnt-use-the-userbot-now">Why you shouldn't use the userbot now?</a>

❓ <a href="https://github.com/ftdot/EasyTl/README.md#what-is-planning-in-this-project">What is planning in this project?</a>

## Usage
Currently, this version is +-stable version. But, you may wait to the stable compiled versions of the **EasyTl-GUI** **v1.4.\***.
Report any bug you found there - https://github.com/ftdot/EasyTl/issues

#### Download the latest version
Go [there](https://github.com/ftdot/EasyTl/tags) and download the latest version (Source code (zip))

1. Unpack archive to any directory.
You can also use the git CLI: `$ git clone --depth 1 --branch <LATEST TAG> https://github.com/ftdot/easytl`
2. Open terminal in the directory `easytl-cli` (if you at the linux, if your platform is windows, open this directory)

### Setup 
To work with the EasyTl you must install required packages and run it by the python 3.11+.
But you can run the installation script, that will do it all work, after that you can use EasyTl.

**WARNING:** You must install the python 3.11 for first. You can do it from it official site: https://www.python.org/

#### For the Linux:

    # ./install.sh

#### For the Windows:

    You must run the install.bat file

### (Optional) Set up the FFMPEG (Need for STTLib plugin)
STTLib plugin is provides "speech to text" functional. To work, it requires FFMPEG.
As example, STTLib required for plugin "VoiceToText", that converts the voice messages and other audio content to the text

**WARNING!:** At the moment support only Debian-based linux systems. Also, to install "ffmpeg" package required root privileges

#### For the Linux (Debian):

    # sudo ./install_ffmpeg.sh

#### For the Windows:

    You must run the install_ffmpeg.bat file

### Set up API_ID, API_HASH and MY_ID in easytl.py
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

#### Fast guide:
* Go to page https://my.telegram.org/
* Authorize with telegram to this page
* Go to Apps tab
* Create app
* Copy a value "API ID", replace `` API_ID = -1`` to the ``API_ID = [Your API ID]``
* Copy a value "API HASH", replace `` API_HASH = ''`` to the ``API_ID = '[Your API HASH]'``
* Go to the telegram and write to the bot [@myidbot](https://t.me/myidbot)
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
* ``uk`` - Ukrainian

### Run it
After you configured the userbot, run that.


#### For the Linux:
```
# python3 easytl.py
```

#### For the Windows:
```
python easytl.py
```

For first run, the userbot will ask you for the credentials (Number and code). This is required to authorize the userbot

## Why you shouldn't use the userbot now?
At the moment it is unstable and not have full documentation and functional, that required for normal work with this project.

You can see my plugins for EasyTl [here](https://github.com/ftdot/easytl-content/tree/main/plugins)

## What is planning in this project?
* Easy PluginAPI (already do)
* Easy utilities as: configs, translations, plugin auto-update (already do)
* Full, easy to read documentation
* Easy to use, cool GUI
* Cross-platform (including Android)
