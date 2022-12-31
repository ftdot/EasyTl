

class PluginError(Exception):
    """Class for all the plugins errors

    :ivar plugin_name: Name of the plugin raised exception
    :type plugin_name: str
    :ivar description: Description of the exception
    :type description: str
    """

    def __init__(self, plugin_name: str, description: str, *args):
        """
        :param plugin_name: Name of the plugin that raises the exception
        :type plugin_name: str
        :param description: Description of the error
        :type description: str
        """
        super().__init__(*args)
        self.plugin_name  = plugin_name
        self.description  = description

    def __str__(self):
        return f'Plugin "{self.plugin_name}" ' + self.description


class PluginRequiresError(PluginError):

    def __init__(self, plugin_name: str, required: str, *args):
        super().__init__(plugin_name, f'requires the "{self.required}" to work', *args)


class PluginExitedError(PluginError):

    def __init__(self, plugin_name: str, *args):
        super().__init__(plugin_name, 'is exited', *args)


class ArgumentTypeCastingError(Exception):
    """Error for the ArgumentParser's type-casts

    :ivar description: Description of the error
    :type description: str
    """

    def __init__(self, description: str, *args):
        """
        :param description: Description of the error
        :type description: str
        """
        super().__init__(*args)

        self.description = description

    def __str__(self):
        return self.description


class IncorrectCommandAliasesError(Exception):
    """Error of the pluginapi.Plugin.command() decorator

    :ivar plugin_name: Name of the plugin
    :type plugin_name: str
    :ivar function_name: Name of the function
    :type function_name: str
    """

    def __init__(self, plugin_name: str, function_name: str,  *args):
        """
        :param plugin_name: Description of the error
        :type plugin_name: str
        :param function_name: Name of the function
        :type function_name: str
        """
        super().__init__(*args)

        self.plugin_name = plugin_name
        self.function_name = function_name

    def __str__(self):
        return f'Plugin "{self.plugin_name}" have function "{self.function_name}()" with incorrect aliases set'
