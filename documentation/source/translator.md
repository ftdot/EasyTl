# EasyTl documentation

## source.translator
`source/translator.py` is a module with `Translator` object, that allows to create 

**File: [src/source/translator.py](../../src/source/translator.py)**

#### Translator `translator.Namespace`
Class that helps replace dict with the sample namespace

> #### Parameters:
>
>> ##### Translator.lang_dir (`str`)
>> Path to the directory with the translation files
>
>> ##### Translator.lang `str`
>> Language (Country code)

> #### Variables of the `Translator`:
>
>> ##### Translator.namespace (`str`)
>> (Link to the) current `Namespace` instance
>
>> ##### Translator.logger (`logging.Logger`)
>> Translator logger

> #### Methods:
>
>> ##### Translator.load_file() `(self, path: str) -> None`
>> Loads file by `path` to the `namespace.translations`
> 
>> ##### Translator.load_languages() `() -> None`
>> Load files by from the `Translator.lang_dir` to the `namespace.translations` by using `Translator.load_file()`
>
>> ##### Translator.initialize() `(head: str) -> None`
>> Load files by from the `Translator.lang_dir` to the `namespace.translations` by using `Translator.load_file()`