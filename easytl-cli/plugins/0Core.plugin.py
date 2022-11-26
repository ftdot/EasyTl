# begin info
#   description = "Core plugin | Basic functional"
#   required_platforms = [ "windows", "linux", "android" ]
#   etl_version_min = [ 1, 4, 0 ]
#   etl_version_max = [ 1, 4, "*" ]
#   version = "1.4"
#   update_link = "no link"
#   lang_links = "no link"
#   requirements = "no requirements"
#   author = "ftdot (https://github.com/ftdot)"
#   changelog = [ "1.4.0 update" ]
# end info

import os
import sys

import math  # for extend the calculator features

# initialize the core translation
namespace.translator.initialize('core')

# get the prefixes
namespace.instance.prefixes = namespace.translations['core']['prefixes']

# write some config values to the namespace
namespace.platform  = namespace.instance.config['build_platform']
namespace.version   = namespace.instance.config['version']

# variables for the commands
logs_dir   = namespace.instance.logs_dir
cache_dir  = namespace.instance.cache_dir

# list with the temp (cache) files
namespace.temp_files = []
# check if namespace.instance_file is set
namespace.instance_file = namespace.instance_file if 'instance_file' in dir(namespace) else None

# check for the ffmpeg
namespace.ffmpeg = False

if sys.platform == 'win32':
    if os.path.exists(namespace.ffmpeg_dir):
        namespace.ffmpeg = True
        os.environ['PATH'] = os.environ['PATH']+';'+os.path.join(namespace.ffmpeg_dir, 'bin')

elif sys.platform == 'linux':
    if os.system('dpkg -l ffmpeg') == 0:
        namespace.ffmpeg = True


# stop the userbot
@this.command(namespace.translations['core']['command']['stop']['names'])
async def stop(event, _):
    this.logger.info('Stopping the instance')

    await namespace.instance.send(
        event,
        namespace.instance.f_warning(namespace.translations['core']['command']['stop']['stop_notify'])
    )
    await namespace.instance.client.disconnect()  # Disconnect from the telegram
    exit()


# restart the userbot
@this.command(namespace.translations['core']['command']['restart']['names'])
async def restart(event, _):
    this.logger.info('Restarting the instance')

    if namespace.instance_file is None:
        this.logger.info('namespace.instance_file not set. Can\'t do restart')
        return

    # notify about the being restart
    await namespace.instance.send(
        event,
        namespace.instance.f_warning(namespace.translations['core']['command']['restart']['restart_notify'])
    )

    command = ' '.join([sys.executable, namespace.instance_file, 'restart'])
    namespace.instance.logger.debug(f'Restart the instance with a command: {command}')

    os.execl(command)  # run instance again
    await namespace.instance.client.disconnect()  # Disconnect from the telegram


# clear the cache of userbot
@this.command(namespace.translations['core']['command']['clear-cache']['names'])
async def clear_cache(event, _):
    this.logger.info('Cleaning the logs')

    for f in [os.path.join(logs_dir, f) for f in os.listdir(logs_dir)] + \
             [os.path.join(cache_dir, f) for f in os.listdir(cache_dir)] + \
             namespace.temp_files:
        if '.gitkeep' in f:  # save ".gitkeep" file
            continue

        # try to remove the file
        try:
            os.remove(f)
        except Exception as e:
            this.logger.debug(f'Can\'t delete file "{f}"')
            this.log_exception(e)

    namespace.temp_files = []

    await namespace.instance.send_success(event, namespace.translations['core']['command']['clear-cache']['cleaned_message'])


# send calculated expression to the current chat
async def calculate(event, expr):
    await namespace.instance.send_success(
        event,
        namespace.translations['core']['command']['calc']['output_message'].format(
            eval(expr)
        )
    )


# calculates the expression
@this.command(namespace.translations['core']['command']['calc']['names'])
async def calc(event, args):

    if event.reply_to:
        # find the "replied to" message
        msg = [msg async for msg in namespace.instance.client.iter_messages(event.chat_id, 25)
                        if msg.id == event.reply_to.reply_to_msg_id]

        # calculate the "replied to" message text
        await calculate(event, msg[0].message)
        return

    # calculate the arguments
    await calculate(event, ' '.join(args[1:]))

namespace.pcommands[calc.__name__].append('danger')  # mark this command as danger


# do nothing
@this.command(namespace.translations['core']['command']['pass']['names'])
async def pass_(_, __):
    this.logger.info('Pass command called. Do nothing :)')
