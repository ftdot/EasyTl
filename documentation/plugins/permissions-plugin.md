# EasyTl documentation

## plugins -> 0Permissions plugin
This is a main plugin with the permissions control functional

**File: [src/plugins/0Permissions.plugin.py](../../src/plugins/0Permissions.plugin.py)**

> #### Commands **EN**
> 
>> ##### `trust` command
>> By this command you can trust any command to any other Telegram user
>>
>> You must reply to users message you want to trust!
>> 
>> Example: `ez trust`

> #### Команды **RU**
> 
>> ##### Команда `доверить`
>> С помощью этой команды вы можете доверить почти любую команду другому пользователю
>>
>> Вам нужно этой командой ответить на сообщение пользователя, которому вы хотите доверить эту команду!
>> 
>> Пример: `изи доверить`

> #### Low level (for developers)
>
>> ##### namespace.call_w_permissions `async (func, event, args) -> None`
>> Function for check the permissions. It is by default is equals to plugins "call_w_permissions()" function
>>
>> Function takes the function to check permissions and call as first argument, telethon event as second and args as third
>>
>> Do not recommend to overwrite this function!