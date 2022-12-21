# EasyTl documentation

## plugins -> 0Core plugin
This is a main plugin with the main functional

**File: [src/plugins/0Core.plugin.py](../../src/plugins/0Core.plugin.py)**

> #### Commands **EN**
> 
>> ##### `stop` command
>> By this command you can stop the EasyTl
>> 
>> Example: `ez restart`
> 
>> ##### `restart` command
>> By this command you can restart the EasyTl
>> 
>> Example: `ez restart`
>
>> ##### `clearcache` command
>> This is clears the actual EasyTl cache
>> 
>> Example: `ez clearcache`, `ez clrcache`
>
>> ##### `calculator` command
>> Allows to calculate any math expression. This command marked as danger, because it is uses `eval()` function
>> 
>> Command supports reply-to-message calculating
>> 
>> Example: `ez calculator 1+2`, `ez calc "math.pi * 12"` or `ez calc` replying to a message with a mathexpression
> 
>> ##### `pass` command
>> This command nothing to do
>> 
>> Example: `ez pass`

> #### Команды **RU**
> 
>> ##### Команда `стоп`
>> С помощью этой команды вы можете легко остановить EasyTl
>> 
>> Пример: `изи стоп`
> 
>> ##### Команда `рестарт`
>> С помощью этой команды вы можете легко перезапустить EasyTl
>> 
>> Пример: `изи рестарт`
>
>> ##### Команда `очисткэш`
>> С помощью этой команды вы можете очистить текущий кэш EasyTl
>> 
>> Пример: `изи очисткэш`
>
>> ##### Команда `обчисл`
>> Позволяет обчислять любые матем. выражения. Эта команда помечена как опасная, потому что использует функцию `eval()`
>> 
>> Команда поддерживает обчисление ответом на сообщение
>> 
>> Пример: `изи обчисл 1+2`, `изи обчисл "math.pi * 12"` или `изи обчисл` отвечая на сообщение с матем. выражением
> 
>> ##### Команда `пасс`
>> Эта команда ничего не делает
>> 
>> Пример: `изи пасс`

> #### Low level (for developers)
>
>> ##### namespace.temp_files `list[str]`
>> List with the temp files to be deleted by `clearcache` command.
>> 
>> It is clears on even usage of the `clearcache` command
> 
>> ##### namespace.platform `str`
>> Shorthand to the `namespace.instance.config['build_platform']`
> 
>> ##### namespace.version `dict[str, Any]`
>> Shorthand to the `namespace.instance.config['version']`
> 
>> ##### namespace.ffmpeg `bool`
>> Indicates that FFMPEG is installed or no