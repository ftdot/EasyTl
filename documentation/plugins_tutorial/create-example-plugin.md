# EasyTl documentation

## Creating of the example plugin

Welcome to this tutorial, now I'm show you how you can develop your own plugin with your own commands!
Let's do it!

**NOTE:** We didn't it tutorial for the newbies in the Python programming!

#### 1. Name and create the plugin
You need to get already installed EasyTl. How to do it [read it](../README.md#user-iconiconsuser-iconpng-users-guide----)

1. Name your plugin.
   > Plugin name must be CamelCase, as example: `MyExample`
   > 
   > We will use the name `MyExample` in our tutorial

2. Create file
   > Go to the `plugins` directory in your `EasyTl` directory and create file with your plugin name.
   > 
   > **NOTE:** Plugins filename must ends with `.plugin.py`, as example: `MyExample.plugin.py`
   > 
   > We will use the filename `MyExample.plugin.py` in the `plugins` directory in our tutorial

#### 2. Set information about it
To know what is plugins version, description, author, requirements, etc. we must set it in the "info lines" of the plugins.

Copy it sample:
```python
# begin info
#   description = ""
#   required_platforms = [ "windows", "linux", "android" ]
#   required_plugins = "no requirements"
#   etl_version_min = [ 1, 4, 0 ]
#   etl_version_max = [ 1, 4, "*" ]
#   version = "1.0.0"
#   update_link = "no link"
#   lang_links = "no link"
#   requirements = "no requirements"
#   author = ""
# end info
```

And fill it with the plugins' information. In our tutorial we create jokes plugin, that uses `pyjokes` plugin package.
Our "info lines" will:
```python
# begin info
#   description = "Adds programmers jokes"
#   required_platforms = [ "windows", "linux", "android" ]
#   required_plugins = "no requirements"
#   etl_version_min = [ 1, 4, 0 ]
#   etl_version_max = [ 1, 4, "*" ]
#   version = "1.0.0"
#   update_link = "no link"
#   lang_links = "no link"
#   requirements = [ "pyjokes" ]
#   author = "ftdot (https://github.com/ftdot)"
# end info
```

> ##### **NOTES:**
> 
>> If you want to add more one requirement of the `requirements` value - use the commas, example:
>> \#  requirements = \[ "colorama", "pyjokes" \]
> 
>> You can add the update link by using the `update_link` value, example:
>> \#  update_link = "https://github.com/ftdot/EasyTl/raw/master/easytl-cli/plugins/0Core.plugin.py"
>
>> You can add translations to your plugin by using the `lang_links`, example:
>> \#   lang_links = \[ \[ "core_en.toml", "https://github.com/ftdot/EasyTl/raw/master/easytl-cli/translations/core_en.toml" ], \[ "core_ru.toml", "https://github.com/ftdot/EasyTl/raw/master/easytl-cli/translations/core_ru.toml" ], \[ "core_uk.toml", "https://github.com/ftdot/EasyTl/raw/master/easytl-cli/translations/core_uk.toml" \] \]
>
>> If your plugin doesn't can run on the `windows`, `linux`, `android` or run only on one platform - use the `required_platforms`, example to support only `windows` platform:
>> \#  required_platforms = \[ "windows" \]

After that we can start the developing

#### 3. Create own command

To create command, we must use the `this.command` decorator. For first - will code our plugin:
```python
# begin info
#   description = "Adds programmers jokes"
#   required_platforms = [ "windows", "linux", "android" ]
#   required_plugins = "no requirements"
#   etl_version_min = [ 1, 4, 0 ]
#   etl_version_max = [ 1, 4, "*" ]
#   version = "1.0.0"
#   update_link = "no link"
#   lang_links = "no link"
#   requirements = [ "pyjokes" ]
#   author = "ftdot (https://github.com/ftdot)"
# end info

import pyjokes  # import the pyjokes package


# generates random joke
def generate_joke():
   return pyjokes.get_joke('en', 'all')  # generate our joke with using pyjokes

# log random joke to the console via plugins logger
this.logger.info(generate_joke())

```

Sample above is doesn't add the commands, only print a random joke to the console. Okay, will add the command now:
```python
... # info lines, imports


@this.command('joke')  # 'joke' - name of the command
async def generate_joke(event, args):
   # NOTE that all commands must be ASYNC. 
   # "event" - is a telethon event (to read about it, you can see the telethon documentation), 
   # "args" - list with the arguments
   joke = pyjokes.get_joke('en', 'all')  # generate our joke with using pyjokes
   
   await namespace.instance.send_success(event, joke)  # send "success" message to the current chat with our joke

```

And if you go to the Telegram and put: `ez joke` it will send to current chat random joke!

#### 4. Add arguments to our command

To add arguments to our command we will use the `ArgumentParser`. We need to import this:
```python
from source.argumentparser import ArgumentParser, Argument, Cast
```

Let's add `ArgumentParser` to our command!:
```python
... # info lines

import pyjokes  # import the pyjokes package
from source.argumentparser import ArgumentParser, Argument, Cast  # import the argument parser


# create our argument parser for the "joke" command
# NOTE: Recommended to not use the variables in argument parser declaration. Use it declaration in the "@this.command" decorator
generate_joke_ap = ArgumentParser(
   this,
   [
      Argument('language', 
               arg_type=Cast.StrCast  # cast to use (it can be IntCast, FloatCast, StrCast, BoolCast, to get detailed read source.argumentparser documentation)
               ),
      Argument('category',  # NOTE: Arguments by default have Cast.StrCast type
               default='all'  # default value of the category. NOTE: Arguments without it automatically required. Arguments that uses it automatically optional
               )
   ]
)


# 'joke' - name of the command
# ap - is the ArgumentParser parameter
@this.command('joke',
              ap=generate_joke_ap)
async def generate_joke(event, args):
   # NOTE: All functions for the commands must be ASYNC. 
   # "event" - is a telethon event (to read about it, you can see the telethon documentation), 
   # "args" - list with the arguments
   language = args.language  # get our "language" argument
   category = args.category  # get our "category" argument
   # NOTE: You mustn't to use variables to get arguments. You can directly to get it, as example:
   # >>> pyjokes.get_joke(args.language, args.category)
   
   joke = pyjokes.get_joke('en', 'all')  # generate our joke with using pyjokes
   
   await namespace.instance.send_success(event, joke)  # send "success" message to the current chat with our joke

```

Recommended to use ArgumentParser insert the "@this.command" decorator. Our code next will be:
```python
... # info lines

import pyjokes  # import the pyjokes package
from source.argumentparser import ArgumentParser, Argument, Cast  # import the argument parser

# 'joke' - name of the command
# ap - is the ArgumentParser parameter
@this.command('joke',
              ap=ArgumentParser(this, [Argument('language', arg_type=Cast.StrCast), Argument('category', default='all')])
              )
async def generate_joke(event, args):
   # NOTE: All functions for the commands must be ASYNC. 
   # "event" - is a telethon event (to read about it, you can see the telethon documentation), 
   # "args" - list with the arguments
   language = args.language  # get our "language" argument
   category = args.category  # get our "category" argument
   # NOTE: You mustn't to use variables to get arguments. You can directly to get it, as example:
   # >>> pyjokes.get_joke(args.language, args.category)
   
   joke = pyjokes.get_joke(language, category)  # generate our joke with using pyjokes
   
   await namespace.instance.send_success(event, joke)  # send "success" message to the current chat with our joke

```

#### 5. Add the translation feature to your plugin

To do this, we need to create translation files:
1. Go to the `translations/` directory
2. Create your `English` translation, named as.. `MyExample_en.toml`
3. Write something that:
   ```toml
   [command.joke]
   names = [ "get-joke", "joke" ]
   ```
   > If you doesn't know about the TOML syntax, [check it](https://toml.io)
   >
   > **NOTE:** dots parses as another dict. Example:
   >> ```toml
   >> [command_joke]
   >> names = [ "generate-joke", "joke" ]
   >> ```
   >> Will be parsed as:
   >> ```python
   >> translated_names = ...['command_joke']['names']
   >> ```
   >> Then:
   >> ```toml
   >> [command.joke]
   >> names = [ "generate-joke", "joke" ]
   >> ```
   >> Will be parsed as:
   >> ```python
   >> translated_names = ...['command']['joke']['names']
   >> ```
4. Then you can translate to the other languages, just change "en" to other langcode. Example: "uk" -> "MyExample_uk.toml"

Then we can work with it.

We need to initialize our translations with `namespace.translator.initialize()`:
```python
# begin info
#   description = "Adds programmers jokes"
#   required_platforms = [ "windows", "linux", "android" ]
#   required_plugins = "no requirements"
#   etl_version_min = [ 1, 4, 0 ]
#   etl_version_max = [ 1, 4, "*" ]
#   version = "1.0.0"
#   update_link = "no link"
#   lang_links = "no link"
#   requirements = [ "pyjokes" ]
#   author = "ftdot (https://github.com/ftdot)"
# end info

import pyjokes  # import the pyjokes package
from source.argumentparser import ArgumentParser, Argument, Cast  # import the argument parser

namespace.translator.intiailize('MyExample')


# namespace.translations['MyExample']['command']['joke']['names'] - names of the command
# ap - is the ArgumentParser parameter
@this.command(namespace.translations['MyExample']['command']['joke']['names'],
              ap=ArgumentParser(this,
                                [Argument('language', arg_type=Cast.StrCast), Argument('category', default='all')])
              )
async def generate_joke(event, args):
    # NOTE: All functions for the commands must be ASYNC.
    # "event" - is a telethon event (to read about it, you can see the telethon documentation),
    # "args" - list with the arguments

    joke = pyjokes.get_joke(args.language, args.category)  # generate our joke with using pyjokes

    await namespace.instance.send_success(event, joke)  # send "success" message to the current chat with our joke

```

That's all you need to know, you can create own cool plugin!

### You may also check it:
* [Telethon documentation](https://docs.telethon.dev)
* [Telethon client reference quick references](https://docs.telethon.dev/en/stable/quick-references/client-reference.html)
* [EasyTl documentation for the developers](../README.md#developers-iconiconsdeveloper-iconpng-for-the-developers)