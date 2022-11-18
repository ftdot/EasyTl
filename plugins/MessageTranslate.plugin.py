# begin info
#   description = "Adds functional to translate the messages"
#   required_platforms = [ "windows", "linux", "android" ]
#   etl_version_min = [ 1, 3, 2 ]
#   etl_version_max = [ 1, 4, "*" ]
#   version = "1.0"
#   update_link = "https://github.com/ftdot/EasyTl/raw/master/plugins/MessageTranslate.plugin.py"
#   lang_links = [ [ "MessageTranslate_en.toml", "https://github.com/ftdot/EasyTl/raw/master/lang/MessageTranslate_en.toml" ], [ "MessageTranslate_ru.toml", "https://github.com/ftdot/EasyTl/raw/master/lang/MessageTranslate_ru.toml" ], [ "MessageTranslate_uk.toml", "https://github.com/ftdot/EasyTl/raw/master/lang/MessageTranslate_uk.toml" ] ]
#   requirements = "no requirements"
#   author = "ftdot (https://github.com/ftdot)"
# end info

if 'translatelib' not in namespace.values:
    this.logger.debug('translatelib not found in the namespace!')
    this.errored = True
    eee()

namespace.translator.initialize('MessageTranslate')


@this.command(namespace.translations['MessageTranslate']['command']['gtranslate']['names'])
async def gtranslate(event, args):
    translate_to = None

    # check the arguments
    if len(args) > 0:
        # check if first argument in the language code
        if args[0] in namespace.translatelib.languages:
            translate_to = args[0]  # set translate to language ...

    # check if the message is "reply to"
    if event.reply_to:
        # find the "reply to" message
        msg = [msg async for msg in namespace.instance.client.iter_messages(event.chat_id, 25)
                        if msg.id == event.reply_to.reply_to_msg_id]
        text = msg.message
    else:
        text = ' '.join(args[1:]) if translate_to else ' '.join(args)

    # set the language, if it not set
    if translate_to is None:
        translate_to = namespace.translator.lang

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
