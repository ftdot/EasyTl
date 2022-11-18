import os
import sys
import traceback
import requests
import pkg_resources
import subprocess
import logging
import tomllib
from .namespace import Namespace
from .utils import VersionCheckOperation, check_version_compatibility, parse_plugin_information
from .filehash import get_file_hash, get_string_hash

required_info_lines = {'description', 'required_platforms', 'etl_version',
                       'version', 'update_link', 'lang_links',
                       'requirements', 'author'}


class Plugin:
    """Base class for the plugins

    :param plugin_name: Name of the plugin
    :type plugin_name: str
    :param plugin_path: Path to the plugin
    :type plugin_path: str

    :ivar active: Is plugin active
    :type active: bool
    :ivar namespace: The global namespace
    :type namespace: Namespace
    :ivar info: Namespace object with the information about the plugin (deprecated version).
                Dict with the info lines of the plugin (v2 format version)
    :type info: Namespace | dict
    :ivar errored: Is plugin raised error
    :type errored: bool
    :ivar logger: Logger instance
    :type logger: logging.Logger
    :ivar activation_steps: Contains the tuples with the FUNCTION and LOG DESCRIPTION
    :type activation_steps: list[tuple[() -> None, str]]
    """

    def __init__(self, plugin_name: str, plugin_path: str):
        self.plugin_name = plugin_name
        self.plugin_path = plugin_path

        self.active = False
        self.namespace = None
        self.info = None

        self.errored = False
        self.logger = logging.Logger(f'EasyTl : Plugin {self.plugin_name}')

        self.activation_steps = [
            (self.check_for_updates, 'Checking for the plugin updates'),
            (self.check_compatibility, 'Checking for the plugin version compatibility'),
            (self.check_requirements, 'Checking for the plugin requirements'),
            (self.execute, 'Executing the plugin')
        ]

    def activate(self):
        """Activates the plugin. Calls the Plugin.check_for_updates(), Plugin.check_requirements(), Plugin.execute()"""

        self.logger.debug('Try to activate the plugin')

        if self.errored or self.active:
            return

        self.logger.info('Trying to enable logging to the stdout')
        if self.namespace.instance.log_plugins_to_stdout():
            self.logger.addHandler(self.namespace.instance.stdout_handler)

        for step in self.activation_steps:
            self.logger.debug('activate() : ' + step[1])
            step[0]()

            if self.errored:
                self.logger.debug('activate() : Error detected, exit from activation_steps cycle')
                return

    ####

    def check_compatibility(self):
        current_version = self.namespace.instance.get_version()['version']['list']

        # get a version min\max support by the format of the info lines
        version_min = self.info['etl_version_min']
        version_max = self.info['etl_version_max']

        if not ((check_version_compatibility(current_version,
                                             version_min,
                                             VersionCheckOperation.GREATER_THAN)
                 or check_version_compatibility(version_min,
                                                current_version,
                                                VersionCheckOperation.EQUALS))
                and (check_version_compatibility(version_max,
                                                 current_version,
                                                 VersionCheckOperation.GREATER_THAN)
                     or check_version_compatibility(version_max,
                                                    current_version,
                                                    VersionCheckOperation.EQUALS))):
            self.logger.error('check_compatibility() : Doesn\'t support this version of the EasyTl')
            self.errored = True

            # write notify about the unsupported version
            self.namespace.notify_stack.append(
                self.namespace.translations['core']['error_notify'].format(
                    self.namespace.translations['core']['pluginapi']['unsupported_version'].format(self.plugin_name)
                )
            )
            return
        self.logger.debug('check_compatibility() : Passed the version check')

    def check_for_updates(self):
        """Does check for the plugin updates"""

        hash_path = os.path.join(self.namespace.instance.cache_dir, self.plugin_name + '.hash')

        self.logger.debug('check_for_updates() : Check for the existing of hash cache of the plugin')

        # check for the hash file
        if not os.path.exists(hash_path):
            # write the sha256 hash of the file in the cache
            with open(hash_path, 'w') as f:
                f.write((fhash := get_file_hash(self.plugin_path)))

        else:
            # read the already cached file hash
            with open(hash_path) as f:
                fhash = f.read()

        self.logger.debug('check_for_updates() : Parsing the info lines of the plugin')
        self.parse_info_v2()

        if self.errored:
            self.logger.debug('check_for_updates() : Error detected')
            return

        try:
            self.logger.debug('check_for_updates() : Try to update the plugin')

            update_link = self.info['update_link']

            # check for update link and save the remote file hash
            if update_link != 'no link':
                self.logger.debug(f'Link found ({update_link}). Sending request')
                r = requests.get(update_link)
                rhash = get_string_hash(r.content)
            else:
                self.logger.debug('Link not setup. Skip the updating')
                rhash = fhash  # write remote hash as local file hash to skip the update

        except Exception as e:
            self.log_exception(e)

            # write notify about the error
            self.namespace.notify_stack.append(
                self.namespace.translations['core']['error_notify'].format(
                    self.namespace.translations['core']['pluginapi']['send_request_error'].format(self.plugin_name)
                )
            )
            self.errored = True
            return

        # compare the local file hash with the remote file hash
        if fhash != rhash:
            self.logger.debug('check_for_updates() : Hash isn\'t equals. Updating the plugin')
            self.logger.debug('check_for_updates() : Writing new content to the plugin file')

            # replace a local plugin with the remote plugin code
            with open(self.plugin_path, 'wb') as f:
                f.write(r.content)

            # Parse info lines
            self.logger.debug('check_for_updates() : Parsing new information about the plugin')
            self.parse_info_v2()

            # check for the error
            if self.errored:
                self.logger.debug('check_for_updates() : Error detected')
                return

            self.logger.debug('check_for_updates() : Downloading the languages for the plugin')
            self.download_languages()

            # check for the error
            if self.errored:
                self.logger.debug('check_for_updates() : Error detected')
                return

            self.logger.debug('check_for_updates() : Add notifies about the update')

            # write notify about updated plugin
            self.namespace.notify_stack.append(
                self.namespace.translations['core']['pluginapi']['update_notify'].format(self.plugin_name)
            )
            self.namespace.notify_stack.append(
                self.namespace.translations['core']['pluginapi']['changelog_notify'].format(
                    self.info['version'], '\n— '.join(self.info['changelog'])
                )
            )

            # Write new hash
            with open(hash_path, 'w') as f:
                f.write(get_file_hash(self.plugin_path))

            return

        self.logger.debug('check_for_updates() : No updates')

    def download_languages(self):
        """Does check for the plugin languages files"""

        languages_link = self.info['lang_links']

        if languages_link == "no link":
            self.logger.debug('download_languages() : No links to the languages')
            return

        try:
            self.logger.debug('download_languages() : Try to download the languages')

            # check for update link and save the remote file hash
            for ll in languages_link:
                lname = ll[0]
                llink = ll[1]
                self.logger.debug(f'download_languages() : Downloading the language "{lname}" ({llink})')

                r = requests.get(llink)

                with open(os.path.join(self.namespace.instance.translator.lang_dir, lname), 'wb') as f:
                    f.write(r.content)

        except Exception as e:
            self.log_exception(e)

            # write notify about the error
            self.namespace.notify_stack.append(
                self.namespace.translations['core']['error_notify'].format(
                    self.namespace.translations['core']['pluginapi']['download_languages_error'].format(
                        self.plugin_name)
                )
            )
            self.errored = True
            return

    def check_requirements(self):
        """Checks the plugin requirements"""

        requirements = self.info['requirements']

        if requirements == 'no requirements':
            self.logger.debug('check_requirements() : Plugin hasn\'t requirements. Skip')
            return

        self.logger.debug('check_requirements() : Requirements are found. Checking it')
        self.logger.debug('check_requirements() : Getting list of the installed packages')

        # define missing packages
        plugin_requirements = set(requirements)
        installed = {pkg.key for pkg in pkg_resources.working_set}
        missing = plugin_requirements - installed

        # check if missing
        if missing:
            self.logger.debug('check_requirements() : Missing are found. Installing it')

            try:
                self.logger.debug('check_requirements() : Installing missing packages: ' + ', '.join(missing))
                # run PIP to install the package
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

            except Exception as e:
                self.log_exception(e)

                # write notify about the error
                self.namespace.notify_stack.append(
                    self.namespace.translations['core']['error_notify'].format(
                        self.namespace.translations['core']['pluginapi']['requirements_error'].format(self.plugin_name)
                    )
                )
                self.errored = True

    def execute(self):
        """Executes the plugin"""

        if self.active:
            return

        self.logger.debug('Executing the plugin')

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
                self.namespace.translations['core']['error_notify'].format(
                    self.namespace.translations['core']['pluginapi']['plugin_execution_error'].format(self.plugin_name)
                )
            )
            self.errored = True

    ####

    def log_exception(self, e: Exception):
        """Logs the exception to the logger

        :param e: Exception to be logged
        :type e: Exception
        """

        self.logger.debug('#' * 25)

        self.logger.error('Exception has been generated, while executing the plugin')
        for line in traceback.format_exception(e):
            self.logger.debug(line.removesuffix('\n'))

        self.logger.debug('#' * 25)

    def parse_info_v2(self):
        """Parses the information about the plugin, or executes old format parsing"""

        with open(self.plugin_path) as f:
            lines = f.read().splitlines()

        is_v2, info = parse_plugin_information(lines)

        if is_v2:
            self.info = info
            return

        self.logger.error('parse_info_v2() : Error! Plugin is using the old v1 format of the info lines')
        self.errored = True

    def command(self, aliases: str | list | None = None):
        """Decorator, that helps register the new command

        :param aliases: Aliases to the command
        :type aliases: str | list | None
        """

        # check if the aliases is a list or string and type-cast it to the list
        aliases = aliases \
            if isinstance(aliases, list) else [aliases, ]

        self.logger.debug('Register the command ALIASES: ' + ', '.join(aliases))

        def deco(func):
            for a in aliases:  # register all aliases to the command
                self.namespace.commands[a] = func

            self.logger.debug('Create permissions list for the function ' + func.__name__)

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

    :ivar logger: Logger instance
    :type logger: logging.Logger
    """

    def __init__(self, plugins: dict[str, Plugin] | None = None, plugins_dir: str = os.path.join('.', 'plugins'),
                 namespace: Namespace | None = None):
        self.plugins = plugins if plugins is not None else {}
        self.plugins_dir = plugins_dir
        self.namespace = namespace if namespace is not None else Namespace()

        self.logger = logging.Logger('EasyTl : PluginsList')

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
                self.logger.error(f'Plugin {plugin_name} return an exception while executing it')

                self.namespace.notify_stack.append(
                    self.namespace.translations['core']['error_notify'].format(
                        self.namespace.translations['core']['pluginapi']['plugin_execution_error'].format('')
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

        self.logger.info('Enabling logging to the stdout')
        self.logger.addHandler(self.namespace.instance.stdout_handler)

        self.logger.info(f'Activating all plugins in the list')

        self.plugins.update(plugins if plugins is not None else {})  # update the plugins list with an argument
        for n, p in self.plugins.items():  # iterate plugins (n - name, p - plugin)
            self.logger.info(f'Activating the plugin {n}')

            p.namespace = self.namespace  # set plugin namespace
            self.activate_plugin(n)
            if p.errored or not p.active:
                self.logger.info(f'Plugin {n} doesn\'t activated')
                continue

            self.logger.info(f'Plugin {n} successfully activated!')
