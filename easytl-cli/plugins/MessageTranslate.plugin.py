# begin info
#   description = "Adds functional to translate the messages"
#   required_platforms = [ "windows", "linux", "android" ]
#   etl_version_min = [ 1, 4, 0 ]
#   etl_version_max = [ 1, 4, "*" ]
#   version = "1.3"
#   update_link = "https://github.com/ftdot/EasyTl/raw/master/plugins/MessageTranslate.plugin.py"
#   lang_links = [ [ "MessageTranslate_en.toml", "https://github.com/ftdot/EasyTl/raw/master/lang/MessageTranslate_en.toml" ], [ "MessageTranslate_ru.toml", "https://github.com/ftdot/EasyTl/raw/master/lang/MessageTranslate_ru.toml" ], [ "MessageTranslate_uk.toml", "https://github.com/ftdot/EasyTl/raw/master/lang/MessageTranslate_uk.toml" ] ]
#   requirements = "no requirements"
#   author = "ftdot (https://github.com/ftdot)"
#   changelog = [ "Support for the 1.4.0 version" ]
# end info

from source.exceptions import ImportLibError

if 'translatelib' not in dir(namespace):
    this.logger.info('translatelib not found in the namespace!')
    this.errored = True

    raise ImportLibError(this.plugin_name, 'translatelib')

namespace.translator.initialize('MessageTranslate')


@this.command(namespace.translations['MessageTranslate']['command']['gtranslate']['names'])
async def gtranslate(event, args):
    translate_to = namespace.translator.lang

    # check the arguments
    if len(args) > 1:
        # check if first argument in the language code
        if args[1] in namespace.translatelib.languages:
            translate_to = args[1]  # set translate to language ...

    # check if the message is "reply to"
    if event.reply_to:
        # find the "reply to" message
        msg = [msg async for msg in namespace.instance.client.iter_messages(event.chat_id, 25)
                        if msg.id == event.reply_to.reply_to_msg_id]
        text = msg[0].message
    else:
        text = ' '.join(args[2:] if len(args) > 1 else args[1:]) if translate_to else ' '.join(args)

    # send translated message
    await namespace.instance.send_success(
        event,
        namespace.translations['MessageTranslate']['command']['gtranslate']['translated_message'].format(
            namespace.translatelib.translate(text, translate_to)
        )
    )


@this.command(namespace.translations['MessageTranslate']['command']['available_langs']['names'])
async def available_langs(event, _):
    await namespace.instance.send_success(
        event,
        namespace.translations['MessageTranslate']['command']['available_langs']['message'].format(
            '\n'.join(
                [f'`{lang[0]}` -- {lang[1]}' for lang in namespace.translatelib.languages.items()]
            )
        )
    )
