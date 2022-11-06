import os
import sys
import traceback
import requests
import pkg_resources
import subprocess
import logging
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

    :ivar active: Is plugin active
    :type active: bool
    :ivar namespace: The global namespace
    :type namespace: Namespace
    :ivar info: Namespace object with the information about the plugin
    :type info: Namespace
    :ivar errored: Is plugin raised error
    :type errored: bool
    :ivar logger: Logger instance
    :type logger: logging.Logger
    """

    def __init__(self, plugin_name: str, plugin_path: str):
        self.plugin_name = plugin_name
        self.plugin_path = plugin_path

        self.active = False
        self.namespace = None
        self.info = None

        self.errored = False
        self.logger = None
        self.logger_prefix = f'PLUGIN {self.plugin_name} : '

    def activate(self):
        """Activates the plugin. Calls the Plugin.check_for_updates(), Plugin.check_requirements(), Plugin.execute()"""

        if self.errored or self.active:
            return

        self.logger = self.namespace.instance.logger

        self.logger.debug(self.logger_prefix + 'Checking for the plugin updates')
        self.check_for_updates()

        self.logger.debug(self.logger_prefix + 'Checking for the plugin requirements')
        self.check_requirements()

        self.logger.debug(self.logger_prefix + 'Executing the plugin')
        self.execute()

    ####

    def check_for_updates(self):
        """Does check for the plugin updates"""

        hash_path = os.path.join(self.namespace.cache_dir, self.plugin_name+'.hash')

        self.logger.debug(self.logger_prefix + 'Check for the existing of hash cache of the plugin')

        if not os.path.exists(hash_path):  # write the sha256 hash of the file in the cache
            with open(hash_path, 'w') as f:
                f.write((fhash := get_file_hash(self.plugin_path)))
        else:  # read the already cached file hash
            with open(hash_path) as f:
                fhash = f.read()

        self.logger.debug(self.logger_prefix + 'Parsing the info lines of the plugin')
        self.parse_info()

        try:
            self.logger.debug(self.logger_prefix + 'Try to update the plugin')

            # check for update link and save the remote file hash
            if self.info.update_link != 'no-link':
                self.logger.debug(self.logger_prefix + 'Link found. Sending request')
                r = requests.get(self.info.update_link)
                rhash = get_string_hash(r.content)
            else:
                self.logger.debug(self.logger_prefix + 'Link not setup. Skip the updating')
                rhash = fhash

        except Exception as e:
            self.log_exception(e)

            # write notify about the error
            self.namespace.notify_stack.append(
                self.namespace.translator.get('core.core.error_notify').format(
                    self.namespace.translator.get('core.plugin_api.send_request_error').format(self.plugin_name)
                )
            )
            self.errored = True
            return

        # compare the local file hash with the remote file hash
        if fhash != rhash:
            self.logger.debug(self.logger_prefix + 'Hash isn\'t equals. Updating the plugin')
            self.logger.debug(self.logger_prefix + 'Writing new content to the plugin file')

            # replace a local plugin with the remote plugin code
            with open(self.plugin_path, 'wb') as f:
                f.write(r.content)

            self.logger.debug(self.logger_prefix + 'Parsing new information about the plugin')
            self.parse_info()

            self.logger.debug(self.logger_prefix + 'Add notifies about the update')

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
            self.logger.debug(self.logger_prefix + 'Plugin hasn\'t requirements. Skip')
            return

        self.logger.debug(self.logger_prefix + 'Requirements are found. Checking it')
        self.logger.debug(self.logger_prefix + 'Getting list of the installed packages')

        # define missing packages
        plugin_requirements = set(self.info.requirements.split('; '))
        installed = {pkg.key for pkg in pkg_resources.working_set}
        missing = plugin_requirements - installed

        # check if missing
        if missing:
            self.logger.debug(self.logger_prefix + 'Missing are found. Installing it')

            try:
                self.logger.debug(self.logger_prefix + 'Installing missing packages: '+', '.join(missing))
                # run PIP to install the package
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

            except Exception as e:
                self.log_exception(e)

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

        self.logger.debug(self.logger_prefix + 'Executing the plugin')

        with open(self.plugin_path) as f:
            code = f.read()

        try:
            # Execute a plugin
            c = exec(compile(code, self.plugin_path, 'exec'), {'namespace': self.namespace, 'this': self})
            self.active = True
        except Exception as e:
            self.log_exception(e)

            # notify about the error
            self.namespace.notify_stack.append(
                self.namespace.translator.get('core.plugin_api.plugin_execution_error').format(self.plugin_name)
            )
            self.errored = True

    ####

    def log_exception(self, e: Exception):
        """Logs the exception to the logger

        :param e: Exception to be logged
        :type e: Exception
        """

        self.logger.debug('#' * 25)

        self.logger.error(self.logger_prefix + 'Exception has been generated, while executing the plugin')
        for line in traceback.format_exception(e):
            self.logger.debug(self.logger_prefix + line.removesuffix('\n'))

        self.logger.debug('#' * 25)

    def parse_info(self):
        """Parses the information about the plugin"""

        self.logger.debug(self.logger_prefix + 'Parsing the information about the plugin')

        # initialize an info namespace, read the file lines
        self.info = Namespace()
        with open(self.plugin_path) as f:
            lines = f.read().splitlines()[:7]

        self.logger.debug(self.logger_prefix + 'Iterate the info lines')

        for ln in lines:  # iterate the file lines
            if not ln.startswith('# '):  # check if the line is a comment
                continue

            # split info line with " := " and add it to the info namespace
            values = ln[2:].split(' := ')
            setattr(self.info, values[0], values[1])

        # check if all required info lines has been indicated
        if required := set(self.info.values.values()) - required_info_lines:
            self.logger.error(self.logger_prefix + 'Required info lines are skipped: '+', '.join(required))
            self.errored = True

    def command(self, aliases: str | list | None = None):
        """Decorator, that helps register the new command

        :param aliases: Aliases to the command
        :type aliases: str | list | None
        """

        # check if the aliases is a list or string and type-cast it to the list
        aliases = aliases \
            if isinstance(aliases, list) else [aliases, ]

        self.logger.debug(self.logger_prefix + 'Register the command ALIASES: '+', '.join(aliases))

        def deco(func):
            for a in aliases:  # register all aliases to the command
                self.namespace.commands[a] = func

            self.logger.debug(self.logger_prefix + 'Create permissions list for the function '+func.__name__)
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
                self.namespace.instance.logger.error(f'PluginList Instance : '
                                                     f'Plugin {plugin_name} return an exception while executing it')

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

        self.namespace.instance.logger.debug(f'PluginList Instance : Activating all plugins in the list')

        self.plugins.update(plugins if plugins is not None else {})  # update the plugins list with an argument

        for n, p in self.plugins.items():  # iterate plugins (n - name, p - plugin)
            self.namespace.instance.logger.debug(f'PluginList Instance : Activating the plugin {n}')

            p.namespace = self.namespace  # set plugin namespace
            self.activate_plugin(n)
