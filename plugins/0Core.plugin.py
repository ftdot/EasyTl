# begin info
#   description = "Core plugin | Basic functional"
#   required_platforms = [ "windows", "linux", "android" ]
#   etl_version_min = [ 1, 3, 0 ]
#   etl_version_max = [ 1, 3, "*" ]
#   version = "1.2"
#   update_link = "no link"
#   lang_links = "no link"
#   requirements = "no requirements"
#   author = "ftdot (https://github.com/ftdot)"
#   changelog = [ "Support for the new version system", "v2 info lines format" ]
# end info

import os
import sys

# initialize the core translation
namespace.translator.initialize('core')

# get the prefixes
namespace.instance.prefixes = namespace.translations['core']['prefixes']

# write some config values to the namespace
namespace.platform  = namespace.instance.get_platform()
namespace.version   = namespace.instance.get_version()

# variables for the commands
logs_dir   = namespace.instance.logs_dir
cache_dir  = namespace.instance.cache_dir

# list with the temp (cache) files
namespace.temp_files = []


# stop the userbot
@this.command(namespace.translations['core']['command']['stop']['names'])
async def stop(event, _):
    namespace.instance.logger.info('Stopping the instance')

    await namespace.instance.send(
        event,
        namespace.instance.f_warning(namespace.translations['core']['command']['stop']['stop_notify'])
    )
    await namespace.instance.client.disconnect()  # Disconnect from the telegram
    exit()


@this.command(namespace.translations['core']['command']['restart']['names'])
async def restart(event, _):
    namespace.instance.logger.info('Restarting the instance')

    # notify about the being restart
    await namespace.instance.send(
        event,
        namespace.instance.f_warning(namespace.translations['core']['command']['restart']['restart_notify'])
    )

    command = ' '.join([sys.executable, namespace.instance_file, 'restart'])
    namespace.instance.logger.debug(f'Restart the instance with a command: {command}')

    os.execl(command)  # run instance again
    await namespace.instance.client.disconnect()  # Disconnect from the telegram


@this.command(namespace.translations['core']['command']['clear-cache']['names'])
async def clear_cache(event, _):
    namespace.instance.logger.info('Cleaning the logs')

    for f in [os.path.join(logs_dir, f) for f in os.listdir(logs_dir)] + \
             [os.path.join(cache_dir, f) for f in os.listdir(cache_dir)] + \
             namespace.temp_files:
        if '.gitkeep' in f:  # save ".gitkeep" file
            continue

        # try to remove the file
        try:
            os.remove(f)
        except:
            pass

    namespace.temp_files = []

    await namespace.instance.send_success(event, namespace.translations['core']['command']['clear-cache']['cleaned_message'])


@this.command(namespace.translations['core']['command']['pass']['names'])
async def pass_(_, __):
    pass
