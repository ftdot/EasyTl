# description := Core plugin | Basic functional
# required_platforms := windows, linux, android
# etl_version := 0
# version := 1.0
# update_link := no-link
# lang_links := no-links
# requirements := no-requirements
# author := ftdot (https://github.com/ftdot)

import sys

# initialize the default translations
namespace.translator.initialize('core')
namespace.translator.initialize('builtin_libs')

# get the prefixes
namespace.instance.prefixes = namespace.translator.get('core.core.prefixes').split('; ')


# stop the userbot
@this.command(namespace.translator.get('core.stop_command.names').split('; '))
async def stop(event, _):
    namespace.instance.logger.info('Stopping the instance')

    await namespace.instance.send(
        event,
        namespace.instance.f_warning(namespace.translator.get('core.stop_command.stop_notify'))
    )
    await namespace.instance.client.disconnect()  # Disconnect from the telegram
    exit()


@this.command(namespace.translator.get('core.restart_command.names').split('; '))
async def restart(event, _):
    namespace.instance.logger.info('Restarting the instance')

    # notify about the being restart
    await namespace.instance.send(
        event,
        namespace.instance.f_warning(namespace.translator.get('core.restart_command.restart_notify'))
    )

    command = ' '.join([sys.executable, namespace.instance_file, 'restart'])
    namespace.instance.logger.debug(f'Restart the instance with a command: {command}')

    os.execl(command)  # run instance again
    await namespace.instance.client.disconnect()  # Disconnect from the telegram


@this.command(namespace.translator.get('core.pass_command.names').split(': '))
async def pass_(_, __):
    pass
