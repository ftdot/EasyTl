# begin info
#   description = "Adds functional to translate the messages"
#   required_platforms = [ "windows", "linux", "android" ]
#   required_plugins = [ [ "1TranslationsLib", "=", [ 1, 3, 0 ] ] ]
#   etl_version_min = [ 1, 4, 0 ]
#   etl_version_max = [ 1, 4, "*" ]
#   version = "1.3.0"
#   update_link = "https://github.com/ftdot/EasyTl/raw/master/easytl-cli/plugins/MessageTranslate.plugin.py"
#   lang_links = [ [ "MessageTranslate_en.toml", "https://github.com/ftdot/EasyTl/raw/master/easytl-cli/translations/MessageTranslate_en.toml" ], [ "MessageTranslate_ru.toml", "https://github.com/ftdot/EasyTl/raw/master/easytl-cli/translations/MessageTranslate_ru.toml" ], [ "MessageTranslate_uk.toml", "https://github.com/ftdot/EasyTl/raw/master/easytl-cli/translations/MessageTranslate_uk.toml" ] ]
#   requirements = "no requirements"
#   author = "ftdot (https://github.com/ftdot)"
#   changelog = [ "Support for the 1.4.0 version" ]
# end info

from source.argumentparser import ArgumentParser, Argument
from source.exceptions import PluginRequiresError

if 'translatelib' not in dir(namespace):
    this.logger.info('translatelib not found in the namespace!')
    this.errored = True

    raise PluginRequiresError(this.plugin_name, 'library: translatelib (1TranslationsLib plugin)')

namespace.translator.initialize('MessageTranslate')

# string with the available languages to translate
languages_string = '\n'.join(
    [f'`{lang[0]}` -- {lang[1]}' for lang in namespace.translatelib.languages.items()]
)


@this.command(namespace.translations['MessageTranslate']['command']['gtranslate']['names'],
              ap=ArgumentParser(this, [Argument('message', default='<<reply_to>>'),
                                       Argument('translate_to', default=namespace.translator.lang)])
              )
async def gtranslate(event, args):
    # check if the message is "reply to"
    if args.message == '<<reply_to>>':
        if not event.reply_to:
            return

        # find the "reply to" message
        msg = [msg async for msg in namespace.instance.client.iter_messages(event.chat_id, 25)
                        if msg.id == event.reply_to.reply_to_msg_id]
        text = msg[0].message
    else:
        text = args.message

    translate_to = args.translate_to.lower()

    if translate_to not in namespace.translatelib.languages:
        await namespace.instance.send_unsuccess(
            event,
            namespace.translations['MessageTranslate']['command']['gtranslate']['invalid_language'].format(
                args.translate_to
            )
        )
        return

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
            languages_string
        )
    )
