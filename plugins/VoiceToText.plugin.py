# begin info
#   description = "Library-plugin | (Speech To Text Lib) Provides functional to generate text from speech"
#   required_platforms = [ "windows", "linux", "android" ]
#   etl_version_min = [ 1, 3, 3 ]
#   etl_version_max = [ 1, 4, "*" ]
#   version = "1.1"
#   update_link = "https://github.com/ftdot/EasyTl/raw/master/plugins/VoiceToText.plugin.py"
#   lang_links = [ ["VoiceToText_en.toml", "https://github.com/ftdot/EasyTl/raw/master/lang/VoiceToText_en.toml"], ["VoiceToText_ru.toml", "https://github.com/ftdot/EasyTl/raw/master/lang/VoiceToText_ru.toml"], ["VoiceToText_uk.toml", "https://github.com/ftdot/EasyTl/raw/master/lang/VoiceToText_uk.toml"] ]
#   requirements = "no requirements"
#   author = "ftdot (https://github.com/ftdot)"
#   changelog = [ "Added offline-translator mode", "Small improvements" ]
# end info

import os

if 'sttlib' not in namespace.values:
    this.logger.info('sttlib not found in the namespace!')
    this.errored = True
    eee()

namespace.translator.initialize('VoiceToText')

# settings

AUTO_STT = False  # on any voice message (only PM) converts it to the text

# advanced settings

temp_file_path = os.path.join(namespace.instance.cache_dir, 'temp.')  # keep the dot at the end!

####


@this.command(namespace.translations['VoiceToText']['command']['vtt']['names'])
async def vtt(event, args):
    translate_from = namespace.translator.lang
    offline = False

    # check the arguments
    if len(args) > 0:

        # check for the offline mode argument
        if args[0] in namespace.translations['VoiceToText']['command']['vtt']['offline_mode_names']:
            offline = True
        else:
            translate_from = args[0]  # set translate to language ...

    if len(args) > 1:
        if args[1] in namespace.translations['VoiceToText']['command']['vtt']['offline_mode_names']:
            offline = True

        # Don't look at this ^)
        if args[1] == 'whowon':
            await namespace.instance.send_success(event, 'Ukraine is won ^)')
            return

    # check if the message is "reply to"
    if event.reply_to:
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

        if not (mime_type := msg.media.document.mime_type.split('/'))[0] == 'audio':
            await namespace.instance.send_unsuccess(
                event,
                namespace.translations['VoiceToText']['command']['vtt']['isnt_audio_message']
            )
            return

        await msg.download_media(temp_file_path+mime_type[1])

        await namespace.instance.send_unsuccess(
            event,
            namespace.translations['VoiceToText']['command']['vtt']['sphinx_success_message' if offline else 'google_success_message']
            .format(
                namespace.sttlib.recognize_speech_from_file(temp_file_path+mime_type[1], offline, translate_from)
            )
        )
        return

    await namespace.instance.send_unsuccess(
        event,
        namespace.translations['VoiceToText']['command']['vtt']['no_reply_to_message']
    )
    return
