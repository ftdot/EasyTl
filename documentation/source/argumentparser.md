# EasyTl documentation

## source.argumentparser
`source/argumentparser.py` is an argument parser that helps to parse the command arguments

**File: [src/source/argumentparser.py](../../src/source/argumentparser.py)**


#### ArgumentParseError `argumentparser.ArgumentParseError`
```python
class ArgumentParseError(Enum)
```

This is enum with the possible argument parser errors


#### ArgTypeCast `argumentparser.ArgTypeCast`
```python
class ArgTypeCast()
```

The base class of the argument type-casts

> #### Parameters
>
>> ##### type\_ (`type`)
>> Type of the argument type-cast

> #### Methods
>
>> ##### ArgTypeCast.typecast() -> `Any`
>> The override function for type-casting from string to ArgTypeCast type.
>> Arguments:
>> - `string` (`str`) - string to be type-casted
>> Returns:
>> - `Any` - type-casted object


#### ListCast\_ `argumentparser.ListCast_`
```python
class ListCast_(ArgTypeCast)
```

Type-cast realization for the list

> #### Parameters
>
>> ##### splitter\_ (`str`)
>> Splitter to split the values from the string
> 
>> ##### values\_type\_ (`ArgTypeCast`)
>> The values type-cast

> #### Methods
>
>> ##### ListCast\_.typecast() -> `list[Any]`
>> Type-casts a string to list type.
>> Arguments:
>> - `string` (`str`) - string to be type-casted
>> Returns:
>> - `list[Any]` - type-casted list object


#### DictCast\_ `argumentparser.DictCast_`
```python
class DictCast_(ArgTypeCast)
```

Type-cast realization for the dict

> #### Parameters
>
>> ##### splitter\_ (`str`)
>> Splitter to split the values from the string
> 
>> ##### kv\_splitter\_ (`str`)
>> Splitter to split the key and value in the string
> 
>> ##### temp\_char (`str`)
>> Temporary character to replace with it "==" and back
> 
>> ##### key\_type (`ArgTypeCast`)
>> Type to type-cast the keys
> 
>> ##### values\_type (`ArgTypeCast`)
>> Type to type-cast the values

> #### Methods
>
>> ##### DictCast\_.typecast() -> `dict[Any, Any]`
>> Type-casts a string to list type.
>> Arguments:
>> - `string` (`str`) - string to be type-casted
>> Returns:
>> - `dict[Any, Any]` - type-casted list object


#### BoolCast `argumentparser.BoolCast`
```python
class BoolCast(ArgTypeCast)
```

Type-cast realization for the bool

> #### Parameters
>
>> ##### true_list (`list[str]`)
>> List with the true strings
> 
>> ##### false_list (`str`)
>> List with the false strings
> 
>> ##### match_case (`bool`)
>> Match case with the true\false lists

> #### Methods
>
>> ##### DictCast\_.typecast() -> `dict[Any, Any]`
>> Type-casts a string to list type.
>> Arguments:
>> - `string` (`str`) - string to be type-casted
>> Returns:
>> - `dict[Any, Any]` - type-casted list object


#### Cast `argumentparser.Cast`
```python
class Cast()
```

Enum with the pre-initialized type-casts

> #### Casts
> There have many pre-initialized type-casts
> 
>> ##### List with all:
>>
>> StrCast - Do nothing, because it is no requirement to type-cast string to the string
>>
>> IntCast - Casts string to `int` type
>>
>> FloatCast - Casts string to `float` type
>>
>> BoolCast - Casts string to `bool` type
>>

> #### Static methods
>
>> ##### setup_bool_cast_translations() `(true_list: list[str], false_list: list[str]) -> None`
>> Set-ups the Cast.BoolCast lists
>>
>>> Arguments:
>>>
>>> true_list (`list[str]`) - list with the true strings
>>>
>>> false_list (`list[str]`) - list with the false strings


#### ListCast `argumentparser.ListCast`
```python
class ListCast()
```

Enum with the pre-initialized list type-casts

> #### Casts
> There have many pre-initialized type-casts
> 
>> ##### List with all:
>>
>> ListStrCast - Generate list with the `str` type values
>>
>> ListIntCast - Generate list with the `int` type values
>>
>> ListFloatCast - Generate list with the `float` type values
>>
>> ListBoolCast - Generate list with the `bool` type values


#### DictCast `argumentparser.DictCast`
```python
class DictCast()
```

Enum with the pre-initialized dict type-casts

> #### Casts
> There have many pre-initialized type-casts
> 
>> ##### List with `str` dict casts:
>>
>> DictStrStrCast - Generate list with the `str` type values and `str` keys
>>
>> DictStrIntCast - Generate list with the `int` type values and `str` keys
>>
>> DictStrFloatCast - Generate list with the `float` type values and `str` keys
>>
>> DictStrBoolCast - Generate list with the `bool` type values and `str` keys
>>
>> ##### List with `int` dict casts:
>>
>> DictIntStrCast - Generate list with the `str` type values and `int` keys
>>
>> DictIntIntCast - Generate list with the `int` type values and `int` keys
>>
>> DictIntFloatCast - Generate list with the `float` type values and `int` keys
>>
>> DictIntBoolCast - Generate list with the `bool` type values and `int` keys
>>

#### Argument `argumentparser.Argument`
```python
class Argument()
```

The base class of the argument type-casts

> #### Parameters
>
>> ##### type_ (`type`)
>> Type of the argument type-cast
> 
>> ##### false_list (`str`)
>> List with the false strings
> 
>> ##### match_case (`bool`)
>> Match case with the true\false lists
> 
>> ##### false_list (`str`)
>> List with the false strings

> #### Methods
>
>> ##### Argument.typecast() -> `Any`
>> The override function for type-casting from string to ArgTypeCast type.
>> Arguments:
>> - `string` (`str`) - string to be type-casted
>> Returns:
>> - `Any` - type-casted object


#### ArgumentParser `argumentparser.ArgumentParser`
```python
class ArgumentParser()
```

Argument parser

> #### Parameters
>
>> ##### parent_plugin `source.pluginapi.Plugin`
>> Parent plugin of this parser
> 
>> ##### arguments (`list[Argument]`)
>> List with the arguments

> #### Methods
>
>> ##### Argument.parse() -> `(bool, Namespace | ArgumentParseError)`
>> The override function for type-casting from string to ArgTypeCast type.
>> Arguments:
>> - `args` (`list[str]`) - list with the arguments
>> Returns:
>> - `(bool, Namespace | ArgumentParseError)` - namespace with the parsed arguments
