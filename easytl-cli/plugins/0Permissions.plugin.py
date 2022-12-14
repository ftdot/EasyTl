# begin info
#   description = "Library-plugin | Allows to manage the commands permissions"
#   required_platforms = [ "windows", "linux", "android" ]
#   required_plugins = "no requirements"
#   etl_version_min = [ 1, 4, 0 ]
#   etl_version_max = [ 1, 4, "*" ]
#   version = "1.4.0"
#   update_link = "https://github.com/ftdot/EasyTl/raw/master/easytl-cli/plugins/0Permissions.plugin.py"
#   lang_links = [ [ "permissions_en.toml", "https://github.com/ftdot/EasyTl/raw/master/easytl-cli/translations/permissions_en.toml" ], [ "permissions_ru.toml", "https://github.com/ftdot/EasyTl/raw/master/easytl-cli/translations/permissions_ru.toml" ], [ "permissions_uk.toml", "https://github.com/ftdot/EasyTl/raw/master/easytl-cli/translations/permissions_uk.toml" ] ]
#   requirements = "no requirements"
#   author = "ftdot (https://github.com/ftdot)"
#   changelog = [ "Support for the new 1.4.0 version" ]
# end info

namespace.translator.initialize('permissions')


async def call_w_permissions(func, event, args: list[str]):
    """(System method) Calls the command (function) with checking the permissions

    :param func: Function
    :type func: function
    :param event: Telethon's event variable
    :param args: List with the arguments
    :type args: list[str]
    """

    user_id = (await event.get_sender()).id

    this.logger.debug(f'call_w_permissions : '
                                    f'Get permissions for the function {func.__name__}() for the user id {user_id}')

    # check the sender id in the commands allowed ids
    if user_id not in namespace.pcommands[func.__name__]:
        this.logger.debug(f'call_w_permissions : '
                          f'User hasn\'t permissions to execute this function')
        return

    this.logger.debug(f'call_w_permissions : '
                      f'Call the function {func.__name__}()')

    await func(event, args)  # call the function


# trusts some command to the user that message was replied
@this.command(namespace.translations['permissions']['command']['trust']['names'])
async def trust(event, args: list[str]):
    if not len(args) > 1:
        return

    # check if first argument is exists in the registered commands
    if not args[1] in namespace.commands:
        return
    fname = namespace.commands[args[1]].__name__

    # check if the command is danger or no
    if 'danger' in namespace.pcommands[fname]:
        await namespace.instance.send_unsuccess(
            event,
            namespace.translations['permissions']['command']['trust']['danger_command_message']
        )
        return

    # find the message that was replied to
    msg = [msg async for msg in namespace.instance.client.iter_messages(event.chat_id, 25)
                    if msg.id == event.reply_to.reply_to_msg_id]

    # check if the message is exists
    if not any(msg):
        return
    if (sender_id := (await msg[0].get_sender()).id) in namespace.pcommands[fname]:
        await namespace.instance.send_success(
            event,
            namespace.translations['permissions']['command']['trust']['already_trusted_message']
        )
        return

    # add user id to the commands trusted ids
    await namespace.instance.send_success(event,
                                          namespace.translations['permissions']['command']['trust']['trusted_message'])
    namespace.pcommands[fname].append(sender_id)

namespace.call_w_permissions = call_w_permissions
