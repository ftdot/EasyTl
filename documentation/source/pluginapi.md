# EasyTl documentation

## source.pluginapi
`source/pluginapi.py` provides functional for the plugin management

**File: [src/source/pluginapi.py](../../src/source/pluginapi.py)**


#### Plugin `pluginapi.Plugin`
```python
class ArgTypeCast()
```

The base class of the argument type-casts

> #### Parameters
>
>> ##### plugin_name (`str`)
>> Name of the plugin
>
>> ##### plugin_path (`str`)
>> Path to the plugin

> #### Attributes of the `Plugin` objects
>
>> ##### active (`bool`)
>> Is the plugin is active
>
>> ##### namespace (`namespace.Namespace`)
>> The global namespace
> 
>> ##### info (`dict[str, Any]`)
>> Dict with the info lines of the plugin
> 
>> ##### errored (`bool`)
>> Is plugin raised error
>
>> ##### logger (`logging.Logger`)
>> Instance of the `Logger`
> 
>> ##### activation_steps (`list[tuple[() -> None, str]]`)
>> Contains the tuples with the FUNCTION and LOG DESCRIPTION

> #### System methods
>
>> ##### activate() `() -> None`
>> Activates the plugin. Calls the functions from `Plugin.activation_steps` list. Takes no arguments (only `self`)
>
>> ##### do_update_only() `() -> None`
>> Updates the plugin. Calls all steps without last. Takes no arguments (only `self`)
>
>> ##### parse_info_v2() `() -> None`
>> Parses the information (v2 format). Takes no arguments (only `self`)
> 
>> ##### download_languages() `() -> None`
>> Does check for the plugin languages files and download it. Takes no arguments (only `self`)
>
>> ##### _convert_operator() `() -> None`
>> Converts chars =, >, < to VersionCheckOperator
>>
>>> ##### Arguments
>>> * `char` (`str`) - char of the operation
>>
>>> ##### Returns
>>> `VersionCheckOperation | None` - VersionCheckOperation if convertion is success, otherwise None
>
>> ##### check_for_updates() `() -> None`
>> Does check for the plugin updates. Takes no arguments (only `self`)
>
>> ##### check_platform() `() -> None`
>> Checks the platform compatibility with the plugin. Takes no arguments (only `self`)
>
>> ##### check_compatibility() `() -> None`
>> Checks the verison compatibility with the plugin. Takes no arguments (only `self`)
> 
>> ##### check_required_plugins() `() -> None`. Takes no arguments (only `self`)
>> Checks for the required plugins. Takes no arguments (only `self`)
> 
>> ##### check_requirements() `() -> None`. Takes no arguments (only `self`)
>> Checks the plugin requirements. Takes no arguments (only `self`)
>
>> ##### execute() `() -> None`. Takes no arguments (only `self`)
>> Executes the plugin. Takes no arguments (only `self`)

> #### Methods for development
>
>> ##### command() `() -> (func) -> func`
>> **Decorator**, that helps register the new command
>>
>>> ##### Arguments
>>> * `aliases` (`str | list | None`) by default is `None` - Aliases to the command
>>> * `ap` (`argumentparser.ArgumentParser | None`) by default is `None` - Argument parser
>>> * `static_pname` (`str | None`), by default is `None` - Static name in the namespace.pcommands dict
>>
>>> ##### Returns
>>> `(func) -> func` - `func` with the changed attributes
>
>> #### only() `(platforms: list[str] | str, alt: ... = lambda: None) -> None`
>> Decorator, that returns function only if concrete platform(s) is supported
>>
>> **NOTE:** If you use this decorator on the "commands" function, and you need to pass nothing as alt function - use `async_empty` as alt function, because it will be called with `await` expression
>>
>>> ##### Arguments
>>> * `platforms` (`list[str] | str`) - Platform(s) that support the function
>>> * `alt` (`argumentparser.ArgumentParser | None`) by default is `() -> None` - Alt function, that will return if it isn't support
>>
>>> ##### Returns
>>> `func | alt` - If platform is supported - decorated function, otherwise - alt function

> #### Static methods
>
>> ##### async_empty() `async () -> None`
>> Do nothing, but this is coroutine. usable for the `only()` method. Takes no arguments


#### PluginsList `pluginapi.PluginsList`
```python
class PluginsList()
```

The base class of the argument type-casts

> #### Parameters
>
>> ##### plugins (`dict[str, Plugin] | None`)
>> Dict with the plugins
>
>> ##### plugins_dir (`str`)
>> Path to the plugin
>
>> ##### namespace (`namespace.Namespace | None`)
>> Global namespace

> #### Attributes of the `PluginList` objects
>
>> ##### plugins (`dict[str, Plugin] | None`)
>> Dict with the plugins.
>> Setups from the `__init__()`
>
>> ##### plugins_dir (`str`)
>> Path to the directory with the plugins.
>> Setups from the `__init__()`
>
>> ##### namespace (`Namespace | None`)
>> Global namespace.
>> Setups from the `__init__()`
>

> #### Methods
> 
>> ##### plugin_is_active() `(plugin_name: str) -> None`
>> Checks if plugin is active
>>
>>> ##### Arguments
>>> * `plugin_name` (`str`) - Name of the plugin
>>
>>> ##### Returns
>>> `bool` - True if the plugin is active. If plugin isn't exists or not active, returns False
> 
>> ##### activate_plugin() `(plugin_name: str, only_update: bool = False) -> None`
>> Activates the plugin
>>
>>> ##### Arguments
>>> * `plugin_name` (`str`) - Name of the plugin
>>> * `only_update` (`bool`) - Only update the plugin
>>
>>> ##### Returns
>>> `bool` - True if plugin is successfully activated
> 
>> ##### update_the_plugins() `() -> None`
>> Updates the plugins. Takes no arguments (only `self`)
> 
>> ##### activate_plugin_list() `(plugins: dict[str, Plugin] | None) -> None`
>> Activates current plugin list
>>
>>> ##### Arguments
>>> * `plugin_name` (`dict[str, Plugin] | None = None`) - Dict of the plugins, that will be added to the current list
