import os
import sys
import traceback
import requests
import pkg_resources
import subprocess
from .namespace import Namespace
from .filehash import get_file_hash


required_info_lines = {'description', 'required_platforms', 'etl_version',
                       'version', 'update_link', 'lang_links',
                       'requirements', 'author'}


class Plugin:
    """Base class of the plugins

    :param plugin_name: Name of the plugin
    :type plugin_name: str
    :param plugin_path: Path to the plugin
    :type plugin_path: str
    """

    def __init__(self, plugin_name: str, plugin_path: str):
        self.plugin_name = plugin_name
        self.plugin_path = plugin_path

        self.active = False
        self.namespace = None
        self.info = None

        self.errored = False

    def activate(self):
        """Activates the plugin. Calls the Plugin.check_for_updates(), Plugin.check_requirements(), Plugin.execute()"""

        if self.errored or self.active:
            return

        self.check_for_updates()
        self.check_requirements()
        self.execute()
    ####

    def check_for_updates(self):
        """Does check for the plugin updates"""

        hash_path = os.path.join(self.namespace.cache_dir, self.plugin_name+'.hash')

        if not os.path.exists(hash_path):  # write the sha256 hash of the file in the cache
            with open(hash_path, 'w') as f:
                f.write((fhash := get_file_hash(self.plugin_path)))
        else:  # read the already cached file hash
            with open(hash_path) as f:
                fhash = f.read()

        self.parse_info()

        try:
            # check for update link and compare the file hash with remote file hash
            if self.info.update_link != 'no-link':
                r = requests.get(self.info.update_link)
                rhash = get_string_hash(r.content)
            else:
                rhash = fhash
        except:
            traceback.print_exc()

            # write notify about the error
            self.namespace.notify_stack.append(
                self.namespace.translator.get('core.core.error_notify').format(
                    self.namespace.translator.get('core.plugin_api.send_request_error').format(self.plugin_name)
                )
            )
            self.errored = True
            return

        if fhash != rhash:
            # replace a local plugin with the remote plugin code
            with open(self.plugin_path, 'wb') as f:
                f.write(r.content)
            self.parse_info()

            # write notify about updated plugin
            self.namespace.notify_stack.append(
                self.namespace.translator.get('core.plugin_api.update_notify').format(self.plugin_name)
            )
            self.namespace.notify_stack.append(
                self.namespace.translator.get('core.plugin_api.changelog_notify').format(self.info.version,
                                                                                         self.info.changelog)
            )
            return

    def check_requirements(self):
        """Checks the plugin requirements"""

        # skip this method, if plugin has error or already active
        if self.errored or self.active:
            return

        if self.info.requirements == 'no-requirements':
            return

        # define if the plugin requirements is missing or no
        plugin_requirements = set(self.info.requirements.split('; '))
        installed = {pkg.key for pkg in pkg_resources.working_set}
        missing = plugin_requirements - installed

        # check if missing
        if missing:
            try:
                # run PIP to install the package
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
            except:
                traceback.print_exc()

                # write notify about the error
                self.namespace.notify_stack.append(
                    self.namespace.translator.get('core.core.error_notify').format(
                        self.namespace.translator.get('core.plugin_api.requirements_error').format(self.plugin_name)
                    )
                )
                self.errored = True

    def execute(self):
        """Executes the plugin"""

        if self.active:
            return

        with open(self.plugin_path) as f:
            code = f.read()

        try:
            # Execute a plugin
            c = exec(code, {'namespace': self.namespace, 'this': self})
            self.active = True
        except Exception:
            traceback.print_exc()

            # notify about the error
            self.namespace.notify_stack.append(
                self.namespace.translator.get('core.plugin_api.plugin_execution_error').format(self.plugin_name)
            )
            self.errored = True

    ####

    def parse_info(self):
        """Parses the information about the plugin"""

        # initialize an info namespace, read the file lines
        self.info = Namespace()
        with open(self.plugin_path) as f:
            lines = f.read().splitlines()[:7]

        for ln in lines:  # iterate the file lines
            if not ln.startswith('# '):  # check if the line is a comment
                continue

            # split info line with " := " and add it to the info namespace
            values = ln[2:].split(' := ')
            setattr(self.info, values[0], values[1])

        # check if all required info lines has been indicated
        if set(self.info.values.values()) - required_info_lines:
            self.errored = True

    def command(self, aliases: str | list | None = None):
        """Decorator, that helps register the new command

        :param aliases: Aliases to the command
        :type aliases: str | list | None
        """

        # check if the aliases is a list or string and type-cast it to the list
        aliases = aliases \
            if isinstance(aliases, list) else [aliases, ]

        def deco(func):
            for a in aliases:  # register all aliases to the command
                self.namespace.commands[a] = func

            # create a function in the commands permissions list
            self.namespace.pcommands[func.__name__] = [self.namespace.instance.owner_id, ]
            return func

        return deco


class PluginsList:
    """Helps work with the plugins list

    :param plugins: Dict with the plugins
    :type plugins: dict[str, Plugin] | None
    :param plugins_dir: Path to the directory with the plugins
    :type plugins_dir: str
    :param namespace: The namespace instance
    :type namespace: Namespace
    """

    def __init__(self, plugins: dict[str, Plugin] | None = None, plugins_dir: str = os.path.join('.', 'plugins'),
                 namespace: Namespace | None = None):
        self.plugins = plugins if plugins is not None else {}
        self.plugins_dir = plugins_dir
        self.namespace = namespace if namespace is not None else Namespace()

    def plugin_is_active(self, plugin_name: str) -> bool:
        """Checks if plugin is active

        :param plugin_name: Name of the plugin
        :type plugin_name: str

        :returns: True if the plugin is active. If plugin isn't exists or not active, returns False
        :rtype: bool
        """

        if plugin_name in self.plugins:
            return self.plugins[plugin_name].active
        return False

    def activate_plugin(self, plugin_name: str) -> bool:
        """Activates the plugin

        :param plugin_name: Name of the plugin
        :type plugin_name: str
        :returns: True if plugin is successfully activated
        :rtype: bool
        """

        if plugin_name in self.plugins:
            p = self.plugins[plugin_name]  # get a plugin from the plugins list
            p.activate()  # activate plugin

            # check if plugin has error
            if p.errored:
                self.namespace.notify_stack.append(
                    self.namespace.translator.get('core.core.error_notify').format(
                        self.namespace.translator.get('core.plugin_api.plugin_execution_error').format('')
                    )
                )
                return False

            return True
        return False

    def activate_plugins_list(self, plugins: dict[str, Plugin] | None = None):
        """Activates current plugin list

        :param plugins: Dict of the plugins, that will be added to the current list
        :type plugins: dict[str, Plugin]
        """

        self.plugins.update(plugins if plugins is not None else {})  # update the plugins list with an argument
        for n, p in self.plugins.items():  # iterate plugins (n - name, p - plugin)
            p.namespace = self.namespace  # set plugin namespace
            self.activate_plugin(n)
