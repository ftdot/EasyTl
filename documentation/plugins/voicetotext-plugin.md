# EasyTl documentation

## plugins -> VoiceToText plugin
Adds to the EasyTl voice to text feature. It uses [1STTLib](../plugins/library-plugins.md#library-plugin-1sttlib)

**File: [src/plugins/VoiceToText.plugin.py](../../src/plugins/VoiceToText.plugin.py)**

> #### Commands **EN**
>
>> ##### `totext` command
>> Recognizes any voice message to the text
>>
>> By optional takes first argument - language to be recognized
>>
>> By optional takes second argument - offline mode or no (yes, no, 1, 0)
>>
>> You must reply with it command to any voice message
>> 
>> Примеры: `ez totext`, `ez vtt uk`

> #### Команды **RU**
>
>> ##### Команда `втекст`
>> Распознаёт любое голосовое сообщение в текст
>>
>> Опционально принимает первый аргумент - язык который будет распознан
>>
>> Опционально принимает второй аргумент - офлайн режим или нет (да, нет, 1, 0)
>>
>> Вы должны отправить эту команду ответом на голосовое сообщение
>> 
>> Примеры: `изи втекст`, `изи втекст en`

> #### Low level (for developers)
>
>> #### This hasn't any except of the commands
