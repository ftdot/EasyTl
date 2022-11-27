
class ImportLibError(Exception):

    def __init__(self, plugin_name, lib_name, *args):
        super().__init__(args)
        self.plugin_name = plugin_name
        self.lib_name = lib_name

    def __str__(self):
        return f'Plugin "{self.plugin_name}" can\'t find the library "{self.lib_name}"'


class RequiredError(Exception):

    def __init__(self, plugin_name, required, *args):
        super().__init__(args)
        self.plugin_name = plugin_name
        self.required = required

    def __str__(self):
        return f'Plugin "{self.plugin_name}" requires the "{required}" to work'


class PluginExitedError(Exception):

    def __init__(self, plugin_name, *args):
        super().__init__(args)
        self.plugin_name = plugin_name

    def __str__(self):
        return f'Plugin "{self.plugin_name}" exited'
