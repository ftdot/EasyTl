

class PluginError(Exception):

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
        return f'Plugin "{self.plugin_name}" '+self.description


class PluginRequiresError(PluginError):

    def __init__(self, plugin_name, required, *args):
        super().__init__(plugin_name, f'requires the "{self.required}" to work', *args)


class PluginExitedError(PluginError):

    def __init__(self, plugin_name, *args):
        super().__init__(plugin_name, 'is exited', *args)