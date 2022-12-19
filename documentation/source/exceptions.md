# EasyTl documentation

## source.exceptions
`source/exceptions.py` is a file with all working exceptions

**File: [src/source/exceptions.py](../../src/source/exceptions.py)**

#### PluginError `exceptions.PluginError`
```python
class PluginError(Exception)
```
Class for all the plugins errors

> #### Parameters:
>
>> ##### PluginError.plugin\_name `str`
>> Name of the plugin
>
>> PluginError.description `str`
>> Description of the error


#### PluginRequiresError `exceptions.PluginRequiresError`
```python
class PluginRequiresError(PluginError)
```

> Parameters:
> 
>> ##### PluginError.plugin\_name `str`
>> Name of the plugin
>
>> ##### PluginError.required `str`
>> A thing required for the plugin


#### PluginExitedError `exceptions.PluginExitedError`
```python
class PluginExitedError(PluginError)
```

> Parameters:
> 
>> ##### PluginError.plugin\_name `str`
>> Name of the plugin


#### ArgumentTypeCastingError `exceptions.ArgumentTypeCastingError`
```python
class ArgumentTypeCastingError(Exception)
```
Error for the ArgumentParser's type-casts

> #### Parameters:
> 
>> ##### PluginError.description `str`
>> Description of the error