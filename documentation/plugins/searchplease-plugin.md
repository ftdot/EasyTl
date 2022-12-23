# EasyTl documentation

## plugins -> SearchPlease plugin
Adds to the EasyTl searching functional (google search, search images, etc.)s

**File: [src/plugins/SearchPlease.plugin.py](../../src/plugins/SearchPlease.plugin.py)**

> #### Commands **EN**
> 
>> ##### `search` command
>> Opens the query in the browser
>>
>> As first arguments takes query
>> 
>> Example: `ez search "Russian war in Ukraine"`
> 
>> ##### `gsearch` command
>> Search query in the Google and send results to current chat
>>
>> As first arguments takes query
>>
>> By optional takes second argument - number of the queries
>> 
>> Examples: `ez gsearch "EasyTl github"`, `ez gsearch "Russian war in Ukraine" 5`
>
>> ##### `gimgsearch` command
>> Search images in the Google and send results to current chat.
>> **WARNING:** I can't improve the small resolution of results
>>
>> As first arguments takes query
>>
>> By optional takes second argument - is number of the images
>> 
>> Examples: `ez gimgsearch "EasyTl github"`, `ez gimgsearch "Russian war in Ukraine" 5`

> #### Команды **RU**
> 
>> ##### Команда `щанайду`
>> Открывает запрос в браузере
>>
>> Первым аргументом принимает запрос
>> 
>> Пример: `изи щанайду "Как не умереть от C++ при изучении"`
> 
>> ##### Команда `найти`
>> Ищет запрос в Google и отправляет результаты в текущий чат
>>
>> Первым аргументом принимает запрос
>>
>> Опционально принимает второй аргумент - число запросов
>> 
>> Примеры: `изи найти "ftdot гитхаб"`, `изи найти Алина 5`
>
>> ##### Команда `найтикартинку`
>> Ищет изображения в Google и отправляет результаты в текущий чат.
>> **ВНИМАНИЕ:** Мы не можем исправить низкое качество изображений
>>
>> Первым аргументом принимает запрос
>>
>> Опционально принимает второй аргумент - число изображений
>> 
>> Примеры: `изи найтиизображение "EasyTl github"`, `изи найтикартинку "Российская война в Украине" 5`

> #### Low level (for developers)
>
>> ##### Settings for the `search`, `gsearch` commands
>> `browsers` (`dict[str, str]`) - Dictionary with the browsers names and their commands to execute it
>> 
>>> ##### Available browsers:
>>> `Default` - Opens default browser
>>>
>>> `Chrome`, `Opera`, `OperaGX`, `Edge`, `FireFox`
>>
>> `search_engines` (`dict[str, str]`) - Dictionary with the search engines names and their links to search
>>
>> `find_browser` (`str`) - Name of the browser to use (It must be in the browsers dictionary)
>>
>> `search_engine` (`str`) - Search engine name to use
>>
>> `gsearch_country` (`str`) - Country to search in (for the `gsearch` command)
>
>> ##### namespace.searchplease `Namespace`
>> Namespace of the plugins backend functions
>
>> ##### namespace.searchplease.google_search_image_by_query `(query: str, count: int = 1, output_dir: str = Instance.cache_dir) -> (counter: int, images: list[str])`
>> Search images in the Google by query
>>
>>> ##### Arguments
>>>
>>> `query` (`str`) - Query to search
>>>
>>> `count` (`int`) - Count of the images to download
>>>
>>> `output_dir` (`str`) - Path to the directory where will be downloaded the images
>>
>>> ##### Returns
>>>
>>> Returns tuple: `(counter: int, images: str)`
>>>
>>> `counter` (`int`) - Counter of the downloaded images
>>>
>>> `images` (`list[str]`) - Names of the downloaded images
>
>> ##### namespace.searchplease.gsearch `googlesearch.search`
>> Function `search` from the `googlesearch` package
