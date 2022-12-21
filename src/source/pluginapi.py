import os
import sys
import requests
import subprocess
import logging
import time

from .namespace import Namespace
from .argumentparser import ArgumentParser
from .utils import VersionCheckOperation, check_version_compatibility, parse_plugin_information, log_exception, \
    install_requirements
from .exceptions import PluginExitedError
from .filehash import get_file_hash, get_string_hash

required_info_lines = {'description', 'required_platforms', 'required_plugins',
                       'etl_version_min', 'etl_version_max', 'version', 'update_link',
                       'lang_links', 'requirements', 'author'}


class Plugin:
    """Base class for the plugins

    :ivar plugin_name: Name of the plugin
    :type plugin_name: str
    :ivar plugin_path: Path to the plugin file
    :type plugin_path: str
    :ivar active: Is the plugin active
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
        """
        :param plugin_name: Name of the plugin
        :type plugin_name: str
        :param plugin_path: Path to the plugin
        :type plugin_path: str
        """

        self.plugin_name = plugin_name
        self.plugin_path = plugin_path

        self.active = False
        self.namespace = None
        self.info = None

        self.errored = False
        self.logger = logging.getLogger(f'EasyTl : Plugin {self.plugin_name}')

        self.activation_steps = [
            (self.check_for_updates, 'Checking for the plugin updates'),
            (self.check_platform, 'Checking for the platform requirements'),
            (self.check_compatibility, 'Checking for the plugin version compatibility'),
            (self.check_required_plugins, 'Checking for the required plugins'),
            (self.check_requirements, 'Checking for the plugin requirements'),
            (self.execute, 'Executing the plugin')
        ]

    def activate(self):
        """Activates the plugin. Calls the functions from Plugin.activation_steps list"""

        self.logger.debug('Try to activate the plugin')

        if self.errored or self.active:
            return

        for step in self.activation_steps:
            self.logger.debug('activate() : ' + step[1])
            step[0]()

            if self.errored:
                self.logger.debug('activate() : Error detected, exit from activation_steps cycle')
                return

    def do_update_only(self):
        """Updates the plugin. Calls all steps without last"""

        self.logger.debug('Try to update the plugin')

        if self.errored or self.active:
            return

        self.logger.info('Trying to enable logging to the stdout')
        if self.namespace.instance.config['log_plugins_to_stdout']:
            self.logger.addHandler(self.namespace.instance.stdout_handler)

        for step in self.activation_steps[:-1]:
            self.logger.debug('do_update_only() : ' + step[1])
            step[0]()

            if self.errored:
                self.logger.debug('do_update_only() : Error detected, exit from activation_steps cycle')
                return

    ####

    def parse_info_v2(self):
        """Parses the information about the plugin"""

        with open(self.plugin_path) as f:
            lines = f.read().splitlines()

        is_v2, info = parse_plugin_information(lines)

        if not is_v2:
            self.logger.error('parse_info_v2() : Error! Plugin is using the old v1 format of the info lines')
            self.errored = True
            return

        self.info = info

        missing = required_info_lines - set(self.info.keys())
        if len(missing) != 0:
            self.logger.error('parse_info_v2() : Plugin is passed required info lines: ' + ' '.join(list(missing)))
            self.errored = True

    def download_languages(self):
        """Does check for the plugin languages files and download it"""

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

                # get request
                r = requests.get(llink)

                # check for the status code
                if not r.status_code != 200:
                    self.logger.debug('download_languages() : Request returned non 200 code')

                    self.namespace.notify_stack.append(
                        self.namespace.translations['core']['error_notify'].format(
                            self.namespace.translations['core']['pluginapi']['send_request_error'].format(
                                self.plugin_name)
                        )
                    )
                    self.errored = True
                    return

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

    def _convert_operator(self, char: str) -> VersionCheckOperation | None:
        """Converts chas =, >, < to VersionCheckOperator

        :param char: Character to be converted
        :type char: str

        :returns: VersionCheckOperation if convertion is success, otherwise None
        :rtype: VersionCheckOperation | None
        """

        match char:
            case '=':
                return VersionCheckOperation.EQUALS
            case '>':
                return VersionCheckOperation.GREATER_THAN
            case '<':
                return VersionCheckOperation.LESS_THAN
            case _:
                self.logger.debug(f'_convert_operator() : Incorrect operator "{char}"')

                # write notify about the error
                self.namespace.notify_stack.append(
                    self.namespace.translations['core']['error_notify'].format(
                        self.namespace.translations['core']['pluginapi']['required_plugin_error'].format(
                            self.plugin_name)
                    )
                )
                self.errored = True
                return

    ####

    def check_for_updates(self):
        """Does check for the plugin updates"""

        if 'enable_plugins_auto_update' not in dir(self.namespace) \
                or not getattr(self.namespace, 'enable_plugins_auto_update', False):
            self.logger.debug('check_for_updates() : Auto-updates is disabled. Parse info lines')
            self.parse_info_v2()
            return

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
                try:
                    r = requests.get(update_link)

                    # check for the success
                    if r.status_code != 200:
                        self.logger.debug('Update request returned non 200 code')
                        rhash = fhash
                    else:
                        rhash = get_string_hash(r.content)
                except Exception as e:
                    log_exception(self.logger, e)

                    self.logger.info('check_for_updates() : Can\'t connect to the update link. Skip the update')
                    rhash = fhash
            else:
                self.logger.debug('Link not setup. Skip the updating')
                rhash = fhash  # write remote hash as local file hash to skip the update

        except Exception as e:
            log_exception(self.logger, e)

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

            try:
                # write notify about the update of plugin
                self.namespace.notify_stack.append(
                    self.namespace.translations['core']['pluginapi']['update_notify'].format(self.plugin_name)
                )

                # check for the changelog info line and add it to the notify stack
                if 'changelog' in self.info:
                    self.namespace.notify_stack.append(
                        self.namespace.translations['core']['pluginapi']['changelog_notify'].format(
                            self.info['version'], '\n— '.join(self.info['changelog'])
                        )
                    )
            except Exception as e:
                self.logger.warning('Can\'t write a notify about the update')

                log_exception(self.logger, e)

            # Write new hash
            with open(hash_path, 'w') as f:
                f.write(get_file_hash(self.plugin_path))

            return

        self.logger.debug('check_for_updates() : No updates')

    def check_platform(self):
        if not self.namespace.instance.config['build_platform'] in self.info['required_platforms']:
            self.logger.debug('check_platform() : Doesn\'t support current platform')

            # write notify about the error
            self.namespace.notify_stack.append(
                self.namespace.translations['core']['error_notify'].format(
                    self.namespace.translations['core']['pluginapi']['platform_error'].format(self.plugin_name)
                )
            )
            self.errored = True
            return

        self.logger.debug('check_platform() : Check passed. Platform is supporting')

    def check_compatibility(self):
        current_version = self.namespace.instance.config['version']['list']

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
                    self.namespace.translations['core']['pluginapi']['unsupported_version_error'].format(
                        self.plugin_name)
                )
            )
            return
        self.logger.debug('check_compatibility() : Passed the version check')

    def check_required_plugins(self):
        required_plugins = self.info['required_plugins']
        if required_plugins == 'no requirements':
            self.logger.debug(f'check_required_plugins() : Plugin hasn\'t requirement for the others plugins')
            return

        current_plugins_list = [p for p in self.namespace.plugins.plugins if self.namespace.plugins.plugins[p].active]

        for rp in required_plugins:
            if isinstance(rp, str):
                if rp not in current_plugins_list:
                    # write notify about the error
                    self.namespace.notify_stack.append(
                        self.namespace.translations['core']['error_notify'].format(
                            self.namespace.translations['core']['pluginapi']['required_plugin_error'].format(
                                self.plugin_name)
                        )
                    )
                    self.errored = True
                    return

            elif isinstance(rp, list):
                rp_name = rp[0]
                rp_operations = [self._convert_operator(c) for c in rp[1]]
                rp_version_list = rp[2]

                if self.errored:
                    return

                if rp_name not in current_plugins_list:
                    self.logger.info(f'Plugin "{self.plugin_name}" requires plugin "{rp_name}"')
                    # write notify about the error
                    self.namespace.notify_stack.append(
                        self.namespace.translations['core']['error_notify'].format(
                            self.namespace.translations['core']['pluginapi']['required_plugin_error'].format(
                                self.plugin_name)
                        )
                    )
                    self.errored = True
                    return

                result = False

                for op in rp_operations:
                    if check_version_compatibility(self.namespace.plugins.plugins[rp_name].info["version"].split('.'),
                                                   rp_version_list,
                                                   op):
                        result = True

                if not result:
                    self.logger.info(f'Plugin "{self.plugin_name}" requires plugin with version {rp[1]} '
                                     f'"{".".join([str(v) for v in rp_version_list])}"')
                    # write notify about the error
                    self.namespace.notify_stack.append(
                        self.namespace.translations['core']['error_notify'].format(
                            self.namespace.translations['core']['pluginapi']['required_plugin_error'].format(
                                self.plugin_name)
                        )
                    )
                    self.errored = True

        self.logger.debug(f'check_required_plugins() : Plugin passed check for the required plugins')

    def check_requirements(self):
        """Checks the plugin requirements"""

        requirements = self.info['requirements']

        if requirements == 'no requirements':
            self.logger.debug('check_requirements() : Plugin hasn\'t requirements. Skip')
            return

        try:
            install_requirements(requirements, self.namespace.instance.logs_dir)
        except Exception as e:
            log_exception(self.logger, e)

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
        except PluginExitedError:
            pass
        except Exception as e:
            log_exception(self.logger, e)

            # notify about the error
            self.namespace.notify_stack.append(
                self.namespace.translations['core']['error_notify'].format(
                    self.namespace.translations['core']['pluginapi']['plugin_execution_error'].format(self.plugin_name)
                )
            )
            self.errored = True

    ####

    def command(self, aliases: str | list | None = None, ap: ArgumentParser | None = None,
                static_pname: str | None = None):
        """Decorator, that helps register the new command

        :param aliases: Aliases to the command
        :type aliases: str | list | None
        :param ap: Argument parser
        :type ap: ArgumentParser | None
        :param static_pname: Static name in the namespace.pcommands dict
        :type static_pname: str | None
        """

        # check if the aliases is a list or string and type-cast it to the list
        aliases = aliases \
            if isinstance(aliases, list) else [aliases, ]

        self.logger.debug('Register the command ALIASES: ' + ', '.join(aliases))

        def deco(func):
            func.ap = ap

            # pname - name in the permissions list
            pname = static_pname if static_pname is not None else func.__name__

            # register all aliases to the command
            for a in aliases:
                self.namespace.commands[a] = func

            self.logger.debug(f'Create permissions list for the function {func.__name__}(), pname: {pname}')

            # create a function in the commands permissions list
            self.namespace.pcommands[pname] = [] + self.namespace.instance.owner_ids
            return func

        return deco

    def only(self, platforms: list[str] | str, alt: ... = lambda: None):
        """Decorator, that helps allow only to concrete platform(s)

        :param platforms: Platforms that support the function
        :type platforms: list[str] | str
        :param alt: Alt function, that will return if it isn't support
        """

        platforms = platform if isinstance(platforms, list) else [platforms]

        def deco(func):
            if self.namespace.platform in platforms:  # check for the platform
                return func
            return alt

        return deco

    @staticmethod
    async def async_empty():
        """Empty async function"""
        pass


class PluginsList:
    """Helps work with the plugins list

    :ivar plugins: Dict with the plugins
    :type plugins: dict[str, Plugin] | None
    :ivar plugins_dir: Path to the directory with the plugins
    :type plugins_dir: str
    :ivar namespace: The namespace instance
    :type namespace: Namespace
    :ivar logger: Logger instance
    :type logger: logging.Logger
    """

    def __init__(self, plugins: dict[str, Plugin] | None = None, plugins_dir: str = os.path.join('.', 'plugins'),
                 namespace: Namespace | None = None):
        """
        :param plugins: Dict with the plugins
        :type plugins: dict[str, Plugin] | None
        :param plugins_dir: Path to the directory with the plugins
        :type plugins_dir: str
        :param namespace: The namespace instance
        :type namespace: Namespace
        """

        self.plugins = plugins if plugins is not None else {}
        self.plugins_dir = plugins_dir
        self.namespace = namespace if namespace is not None else Namespace()

        self.logger = logging.getLogger('EasyTl : PluginsList')

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

    def activate_plugin(self, plugin_name: str, only_update: bool = False) -> bool:
        """Activates the plugin

        :param plugin_name: Name of the plugin
        :type plugin_name: str
        :param only_update: Only update the plugin
        :type only_update: bool

        :returns: True if plugin is successfully activated
        :rtype: bool
        """

        if plugin_name in self.plugins:
            p = self.plugins[plugin_name]  # get a plugin from the plugins list
            p.activate()  # activate plugin

            # check if plugin has error
            if p.errored:
                self.logger.error(f'Plugin {plugin_name} return an exception while executing it')
                return False

            return True
        return False

    ####

    def update_the_plugins(self):
        """Updates the plugins"""

        self.logger.info('Updating the plugins')

        # iterate the plugins
        for n, p in self.plugins.items():
            self.logger.info(f'Updating the plugin {n}')

            # do only update
            self.activate_plugin(n, only_update=True)
            if p.errored or not p.active:
                self.logger.info(f'Plugin {n} doesn\'t updated')
                continue

            self.logger.info(f'Plugin {n} successfully updated!')

    def activate_plugins_list(self, plugins: dict[str, Plugin] | None = None):
        """Activates current plugin list

        :param plugins: Dict of the plugins, that will be added to the current list
        :type plugins: dict[str, Plugin]
        """

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
