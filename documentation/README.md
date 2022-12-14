# EasyTl documentation
**WARNING!** Documentation can be wrong.
Any issue you can describe [there](https://github.com/ftdot/EasyTl/issues)


## ![User icon](icons/user-icon.png) Users guide | Туториал для пользователей
- ![Guide icon](icons/guide-icon.png) [Installation](userguide/installation.md) 
- - ![Windows icon](icons/windows-icon.png) [Installation on Windows](userguide/installation.md#installation-on-windows)
- - ![Linux icon](icons/linux-icon.png) [Installation on Linux](userguide/installation.md#installation-on-linux)
- ️![Settings icon](icons/settings-icon.png) [Configuration](userguide/configuration.md) 
- **IMPORTANT** | **ВАЖНО** [Small usage guide | Маленький гайд по использованию](userguide/usage.md)


## ![Plugin icon](icons/plugin-icon.png) Plugins documentation (and usage) | Использование плагинов

- [Core plugin (`0Core`)](plugins/core-plugin.md)
- - ![Command icon](icons/cmd-icon.png) [Commands **EN**](plugins/core-plugin.md#commands-en)
- - ![Command icon](icons/cmd-icon.png) [Команды **РУ**](plugins/core-plugin.md#команды-ru)
- - ![Developers icon](icons/developer-icon.png) [Low level (for the developers)](plugins/core-plugin.md#low-level-for-developers)

- [Permissions plugin (`0Permissions`)](plugins/permissions-plugin.md)
- - ![Command icon](icons/cmd-icon.png) [Commands **EN**](plugins/permissions-plugin.md#commands-en)
- - ![Command icon](icons/cmd-icon.png) [Команды **РУ**](plugins/permissions-plugin.md#команды-ru)
- - ![Developers icon](icons/developer-icon.png) [Low level (for the developers)](plugins/permissions-plugin.md#low-level-for-developers)

- [SearchPlease plugin](plugins/searchplease-plugin.md)
- - ![Command icon](icons/cmd-icon.png) [Commands **EN**](plugins/searchplease-plugin.md#commands-en)
- - ![Command icon](icons/cmd-icon.png) [Команды **РУ**](plugins/searchplease-plugin.md#команды-ru)
- - ![Developers icon](icons/developer-icon.png) [Low level (for the developers)](plugins/searchplease-plugin.md#low-level-for-developers)

- [MessageTranslate plugin](plugins/messagetranslate-plugin.md)
- - ![Command icon](icons/cmd-icon.png) [Commands **EN**](plugins/messagetranslate-plugin.md#commands-en)
- - ![Command icon](icons/cmd-icon.png) [Команды **РУ**](plugins/messagetranslate-plugin.md#команды-ru)
- - ![Developers icon](icons/developer-icon.png) [Low level (for the developers)](plugins/messagetranslate-plugin.md#low-level-for-developers)

- [VoiceToText plugin](plugins/voicetotext-plugin.md)
- - ![Command icon](icons/cmd-icon.png) [Commands **EN**](plugins/voicetotext-plugin.md#commands-en)
- - ![Command icon](icons/cmd-icon.png) [Команды **РУ**](plugins/voicetotext-plugin.md#команды-ru)
- - ![Developers icon](icons/developer-icon.png) [Low level (for the developers)](plugins/voicetotext-plugin.md#low-level-for-developers)

- [Library-plugins (For the developers)](plugins/library-plugins.md)
- - [About it](plugins/library-plugins.md#library-plugins)
- - ![Plugin icon](icons/plugin-icon.png) [Library-plugin `1STTLib`](plugins/library-plugins.md#library-plugin-1sttlib)
- - ![Plugin icon](icons/plugin-icon.png) [Library-plugin `1TranslationsLib`](plugins/library-plugins.md#library-plugin-1translationslib)


## ![Developers icon](icons/developer-icon.png) For the developers
[**Create example plugin tutorial**](plugins_tutorial/create-example-plugin.md)


### [source.core](source/core.md)

- [`source.core.Instance`](source/core.md#instance-coreinstance)
- - [`source.core.Instance Parameters + variables`](source/core.md#parameters--variables)
- - [`source.core.Instance Variables`](source/core.md#variables-of-the-instance)
- - [`source.core.Instance Methods`](source/core.md#methods-of-the-instance)
- - [`source.core.Instance Static methods, formatters`](source/core.md#static-methods-formatters)
- - [`source.core.Instance Wrappers to send the messages`](source/core.md#wrappers-to-send-the-messages)


### [source.exceptions](source/exceptions.md)

- [`source.exceptions.PluginError`](source/exceptions.md#pluginerror-exceptionspluginerror)
- - [`source.exceptions.PluginError Parameters`](source/exceptions.md#parameters)

- [`source.exceptions.PluginRequiresError`](source/exceptions.md#pluginrequireserror-exceptionspluginrequireserror)
- - [`source.exceptions.PluginRequiresError Parameters`](source/exceptions.md#parameters-1)

- [`source.exceptions.PluginExitedError`](source/exceptions.md#pluginexitederror-exceptionspluginexitederror)
- - [`source.exceptions.PluginExitedError Parameters`](source/exceptions.md#parameters-2)

- [`source.exceptions.ArgumentTypeCastingError`](source/exceptions.md#argumenttypecastingerror-exceptionsargumenttypecastingerror)
- - [`source.exceptions.ArgumentTypeCastingError Parameters`](source/exceptions.md#parameters-3)


### [source.filehash](source/filehash.md)

- [`source.filehash Functions`](source/filehash.md#functions-of-the-filehash-module)


### [source.namespace](source/namespace.md)

- [`source.namespace.Namespace`](source/namespace.md#namespace-namespacenamespace)
- - [`source.namespace.Namespace Parameters`](source/namespace.md#parameters)
- - [`source.namespace.Namespace Variables`](source/namespace.md#variables-of-the-namespace)


### [source.translator](source/translator.md)

- [`source.translator.Translator`](source/translator.md#translator-translatornamespace)
- - [`source.translator.Translator Parameters`](source/translator.md#parameters)
- - [`source.translator.Translator Methods`](source/translator.md#methods)


### [source.argumentparser](source/argumentparser.md)

- [`source.argumentparser.ArgumentParseError`](source/argumentparser.md#argumentparseerror-argumentparserargumentparseerror)
- - [`source.argumentparser.ArgumentParseError Values`](source/argumentparser.md#values)

- [`source.argumentparser.ArgTypeCast`](source/argumentparser.md#argtypecast-argumentparserargtypecast)
- - [`source.argumentparser.ArgTypeCast Parameters`](source/argumentparser.md#parameters)
- - [`source.argumentparser.ArgTypeCast Methods`](source/argumentparser.md#methods)

- [`source.argumentparser.ListCast_`](source/argumentparser.md#listcast_-argumentparserlistcast_)
- - [`source.argumentparser.ListCast_ Parameters`](source/argumentparser.md#parameters-1)
- - [`source.argumentparser.ListCast_ Methods`](source/argumentparser.md#methods-1)

- [`source.argumentparser.DictCast_`](source/argumentparser.md#dictcast_-argumentparserdictcast_)
- - [`source.argumentparser.DictCast_ Parameters`](source/argumentparser.md#parameters-2)
- - [`source.argumentparser.DictCast_ Methods`](source/argumentparser.md#methods-2)

- [`source.argumentparser.Cast`](source/argumentparser.md#cast-argumentparsercast)
- - [`source.argumentparser.Cast Casts`](source/argumentparser.md#casts)

- [`source.argumentparser.ListCast`](source/argumentparser.md#listcast-argumentparserlistcast)
- - [`source.argumentparser.ListCast Casts`](source/argumentparser.md#casts-1)

- [`source.argumentparser.DictCast`](source/argumentparser.md#dictcast-argumentparserdictcast)
- - [`source.argumentparser.DictCast Casts`](source/argumentparser.md#casts-2)

- [`source.argumentparser.Argument`](source/argumentparser.md#argument-argumentparserargument)
- - [`source.argumentparser.Argument Parameters`](source/argumentparser.md#parameters-3)
- - [`source.argumentparser.Argument Methods`](source/argumentparser.md#methods-3)

- [`source.argumentparser.ArgumentParser`](source/argumentparser.md#argumentparser-argumentparserargumentparser)
- - [`source.argumentparser.ArgumentParser Parameters`](source/argumentparser.md#parameters-4)
- - [`source.argumentparser.ArgumentParser Methods`](source/argumentparser.md#methods-4)

### [source.pluginapi](source/pluginapi.md)

- [`source.pluginapi.Plugin`](source/pluginapi.md#plugin-pluginapiplugin)
- - [`source.pluginapi.Plugin Parameters`](source/pluginapi.md#parameters)
- - [`source.pluginapi.Plugin System methods`](source/pluginapi.md#system-methods)
- - [`source.pluginapi.Plugin Methods for the plugins development`](source/pluginapi.md#methods-for-the-plugins-development)

- [`source.pluginapi.PluginsList`](source/pluginapi.md#pluginslist-pluginapipluginslist)
- - [`source.pluginapi.PluginsList Parameters`](source/pluginapi.md#parameters-1)
- - [`source.pluginapi.PluginsList Methods`](source/pluginapi.md#methods)