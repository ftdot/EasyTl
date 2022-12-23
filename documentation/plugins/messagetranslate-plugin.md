# EasyTl documentation

## plugins -> MessageTranslate plugin
Adds to the EasyTl translation feature. It uses [1TranslationsLib](../plugins/library-plugins.md#library-plugin-1translationslib)

**File: [src/plugins/MessageTranslate.plugin.py](../../src/plugins/MessageTranslate.plugin.py)**

> #### Commands **EN**
>
>> ##### `gtranslate` command
>> Translates text by using the Google Translate services
>>
>> As first arguments takes text to be translate
>>
>> By optional takes second argument - language to be translated into
>> 
>> Examples: `ez gtranslate "Привіт, мене звати Валера і я маю дуже багато дівчин"`, `ez gtrans "I'm using the EasyTl!" es`
>
>> ##### `knownlangs` command
>> Shows available languages to translate into\from
>> 
>> Пример: `ez knownlangs`

> #### Команды **RU**
>
>> ##### Команда `перевести`
>> Переводит текст с помощью Google Translate сервисов
>>
>> Первым аргументом принимает текст который нужно перевести
>>
>> Опционально принимает второй аргумент - язык на который нужно перевести
>> 
>> Примеры: `изи перевести "Привіт, мене звати Валера і я маю дуже багато дівчин"`, `изи перевести "Я использую EasyTl!" es`
>
>> ##### Команда `доступязыки`
>> Показывает доступные языки для перевода \ перевода из
>> 
>> Пример: `изи доступязыки`

> #### Low level (for developers)
>
>> #### This hasn't any except of the commands
