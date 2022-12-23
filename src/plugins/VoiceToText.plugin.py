# begin info
#   description = "Library-plugin | (Speech To Text Lib) Provides functional to generate text from speech"
#   required_platforms = [ "windows", "linux", "android" ]
#   required_plugins = [ "1STTLib" ]
#   etl_version_min = [ 1, 4, 0 ]
#   etl_version_max = [ 1, 4, "*" ]
#   version = "1.2.0"
#   update_link = "https://github.com/ftdot/EasyTl/raw/master/easytl-cli/plugins/VoiceToText.plugin.py"
#   lang_links = [ ["VoiceToText_en.toml", "https://github.com/ftdot/EasyTl/raw/master/easytl-cli/translations/VoiceToText_en.toml"], ["VoiceToText_ru.toml", "https://github.com/ftdot/EasyTl/raw/master/easytl-cli/translations/VoiceToText_ru.toml"], ["VoiceToText_uk.toml", "https://github.com/ftdot/EasyTl/raw/master/easytl-cli/translations/VoiceToText_uk.toml"] ]
#   requirements = "no requirements"
#   author = "ftdot (https://github.com/ftdot)"
#   changelog = [ "Support for the 1.4.0 version" ]
# end info

import os
from source.argumentparser import ArgumentParser, Argument, Cast
from source.exceptions import PluginRequiresError

if 'sttlib' not in dir(namespace):
    this.logger.info('sttlib not found in the namespace!')
    this.errored = True

    raise PluginRequiresError(this.plugin_name, 'library: sttlib (1STTLib plugin)')

namespace.translator.initialize('VoiceToText')

# advanced settings

temp_file_path = os.path.join(namespace.instance.cache_dir, 'temp.')  # keep the dot at the end!

####


@this.command(namespace.translations['VoiceToText']['command']['vtt']['names'],
              ap=ArgumentParser(this, [Argument('translate_from', default=namespace.translator.lang),
                                       Argument('offline', Cast.BoolCast, default=False)])
              )
async def vtt(event, args):
    # check if the message is "reply to"
    if not event.reply_to:
        await namespace.instance.send_unsuccess(
            event,
            namespace.translations['VoiceToText']['command']['vtt']['no_reply_to_message']
        )
        return

    # find the "reply to" message
    msg = [msg async for msg in namespace.instance.client.iter_messages(event.chat_id, 25)
                    if msg.id == event.reply_to.reply_to_msg_id]
    msg = msg[0]

    if not msg.media:
        await namespace.instance.send_unsuccess(
            event,
            namespace.translations['VoiceToText']['command']['vtt']['no_media_message']
        )
        return

    # check if message media content is audio
    if not (mime_type := msg.media.document.mime_type.split('/'))[0] == 'audio':
        await namespace.instance.send_unsuccess(
            event,
            namespace.translations['VoiceToText']['command']['vtt']['isnt_audio_message']
        )
        return

    # download the message media
    await msg.download_media(temp_file_path+mime_type[1])

    # send message with the recognized speech
    await namespace.instance.send_success(
        event,
        namespace.translations['VoiceToText']['command']['vtt']['sphinx_success_message' if args.offline else 'google_success_message']
        .format(
            namespace.sttlib.recognize_speech_from_file(temp_file_path+mime_type[1], args.offline, args.translate_from)
        )
    )
    return

