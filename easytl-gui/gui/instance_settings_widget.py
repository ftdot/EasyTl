import os
import sys
import tomllib
import subprocess
import threading
import logging

from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject

from .window.instanceSettingsWidget import Ui_instanceSettingsWidget
from settings import *

from sourcegui.utils import QuickMessageBox, load_instances_list, save_instances_list


class InstanceSettingsWidget(QtWidgets.QWidget):
    """Functional defines for Instance Settings UI

    :ivar logger: Logger instance
    :type logger: logging.Logger
    :ivar ui: Ui_instanceSettingsWidget instance
    :type ui: Ui_instanceSettingsWidget
    :ivar instances: Dict with the instances
    :type instances: dict[str, Any]
    :ivar allowed_instances_chars: String with only allowed characters for instances names
    :type allowed_instances_chars: str
    :ivar run_instance_wrapper: The run instance wrapper that must be bind to InstanceRollingWidget
    :type run_instance_wrapper: (str) -> None
    :ivar save_vars_dict: Dict with the (config value): (string to eval) elements to save the settings
    :type save_vars_dict: dict[str, str]
    :ivar warning_qmsgbox: QuickMessageBox instance with Warning icon and Ok button
    :type warning_qmsgbox: QuickMessageBox
    :ivar critical_qmsgbox: QuickMessageBox instance with Critical icon and Ok button
    :type critical_qmsgbox: QuickMessageBox
    :ivar information_qmsgbox: QuickMessageBox instance with Information icon and Ok button
    :type information_qmsgbox: QuickMessageBox
    """

    def __init__(self, parent: QObject):
        super().__init__(parent)

        self.logger  = logging.getLogger('EasyTl-GUI : InstanceSettingsWidget')
        self.ui      = None

        self.instances                = {}
        self.allowed_instances_chars  = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890_'
        self.run_instance_wrapper     = lambda _: None

        self.save_vars_dict = {
            'api_id': 'self.ui.apiIdEdit.text()',
            'api_hash': 'self.ui.apiHashEdit.text()',
            'owner_id': 'self.ui.ownerIdEdit.text()',

            'enable_pl_auto_update': 'self.ui.enablePLAutoUpdateChB.isChecked()',
            'logging_level': 'self.ui.loggingLevelCB.currentText()',
            'console_logging_level': 'self.ui.consoleLoggingLevelCB.currentText()'
        }

        self.warning_qmsgbox      = QuickMessageBox(self, QtWidgets.QMessageBox.Warning, QtWidgets.QMessageBox.Ok)
        self.critical_qmsgbox     = QuickMessageBox(self, QtWidgets.QMessageBox.Critical, QtWidgets.QMessageBox.Ok)
        self.information_qmsgbox  = QuickMessageBox(self, QtWidgets.QMessageBox.Information, QtWidgets.QMessageBox.Ok)

    def initialize(self):
        """Initializes the widget"""

        self.logger.debug('Initializing the ui')

        # set up UI
        self.ui = Ui_instanceSettingsWidget()
        self.ui.setupUi(self)

        self.logger.debug('Initializing the connections')

        # initialize connections
        self.ui.instancesList.currentItemChanged.connect(
            lambda: self.load_instance_settings(self.ui.instancesList.currentItem().text())
        )
        self.ui.saveSettingsButton.clicked.connect(self.save_instance_settings)
        self.ui.newInstanceButton.clicked.connect(self.create_new_instance)
        self.ui.removeInstanceButton.clicked.connect(self.remove_current_instance)
        self.ui.runInstanceButton.clicked.connect(self.run_current_instance)

        self.logger.debug('Reset the items')

        # reset items, cmon
        self.reset_items()

        self.ui.instancesList.addItem(QtWidgets.QListWidgetItem('Empty'))

        self.logger.debug('Loading instances list')

        # load instances list and add it to... instances list
        self.instances = load_instances_list()
        for instance_name in self.instances.keys():
            self.ui.instancesList.addItem(QtWidgets.QListWidgetItem(instance_name))

        self.logger.debug('Done')

    ####

    def reset_items(self):
        """Resets the UI items"""

        self.ui.instanceName.setText('No instance')
        self.ui.apiIdEdit.setText('')
        self.ui.apiHashEdit.setText('')
        self.ui.ownerIdEdit.setText('')

        self.ui.enablePLAutoUpdateChB.setChecked(True)
        self.ui.loggingLevelCB.setCurrentText('INFO')
        self.ui.consoleLoggingLevelCB.setCurrentText('As logging level')

    ####

    def load_instance_settings(self, instance_name: str):
        """Loads the settings for the instance by name

        :param instance_name: Name of the instance
        :type instance_name: str
        """

        self.logger.debug('Try to load the instance settings')

        if instance_name == 'Empty':
            self.logger.debug('Empty detected. Reset items and set name')
            self.reset_items()
            self.ui.instanceName.setText('Empty instance (can\'t to be saved and used!)')
            return

        self.reset_items()
        self.ui.instanceName.setText(instance_name)

        if instance_name not in self.instances:
            self.logger.debug(f'The instances list doesn\'t contains the "{instance_name}" instance')
            return

        self.logger.debug('Loading the instance settings')

        self.ui.apiIdEdit.setText(self.instances[instance_name]['api_id'])
        self.ui.apiHashEdit.setText(self.instances[instance_name]['api_hash'])
        self.ui.ownerIdEdit.setText(self.instances[instance_name]['owner_id'])

        self.ui.enablePLAutoUpdateChB.setChecked(self.instances[instance_name]['enable_pl_auto_update'])
        self.ui.loggingLevelCB.setCurrentText(self.instances[instance_name]['logging_level'])
        self.ui.consoleLoggingLevelCB.setCurrentText(self.instances[instance_name]['console_logging_level'])

        self.logger.debug('Done')

    def save_instance_settings(self):
        """Saves the settings for instance"""

        self.logger.debug('Try to save the instances')

        current_instance_name = self.ui.instancesList.currentItem().text()

        if current_instance_name == 'Empty':
            return

        self.logger.debug('Checking for the disallowed characters in the instance name')

        # check for the disallowed characters
        for char in current_instance_name:
            if char not in self.allowed_instances_chars:
                self.critical_qmsgbox.show(
                    'Disallowed characters',
                    f'Name "{current_instance_name}" is incorrect, because contains disallowed characters. '
                    'Instance isn\'t saved!'
                )
                return

        self.logger.debug('Checking for the Owner ID is numeric')

        # check for the api id, owner id is numeric

        if not self.ui.ownerIdEdit.text().isnumeric():
            self.critical_qmsgbox.show(
                'Disallowed characters',
                'Owner ID value is incorrect, because contains disallowed characters. '
                'Instance isn\'t saved!'
            )
            return

        self.logger.debug('Checking for the API ID is numeric')

        if not self.ui.apiIdEdit.text().isnumeric():
            self.critical_qmsgbox.show(
                'Disallowed characters',
                'API ID value is incorrect, because contains disallowed characters. '
                'Instance isn\'t saved!'
            )
            return

        self.logger.debug('Checking for the new instance')

        # check for the new instance
        if current_instance_name not in self.instances:
            self.logger.debug('Creating new instance in instances list')
            self.instances[current_instance_name] = {}

        self.logger.debug('Configure all values')

        # set all config values
        for config_value, eval_value in self.save_vars_dict.items():
            self.instances[current_instance_name][config_value] = eval(eval_value)

        self.logger.debug('Dumping to the file')

        # dump the instances to toml file
        save_instances_list(self.instances)

        self.logger.debug('Done')

        # create message of success save
        self.information_qmsgbox.show('Success save', f'Instance "{current_instance_name}" successfully saved!')

    def create_new_instance(self):
        """Creates the new instance in the instances list (to save there save_instance_settings())"""

        self.logger.debug('Creating new instance')
        self.logger.debug('Getting the instance name')

        instance_name, success = QtWidgets.QInputDialog.getText(
            self,
            'New instance',
            'Enter new instance name:'
        )

        if not success:
            self.logger.debug('Unsuccessful getting the instance name')
            return

        self.logger.debug('Success')

        # check for the disallowed characters
        self.logger.debug('Checking for the disallowed characters')

        for char in instance_name:
            if char not in allowed_instances_chars:
                self.critical_qmsgbox.show(
                    'Disallowed characters',
                    f'Name "{instance_name}" is incorrect, because contains disallowed characters. '
                    'Instance isn\'t saved!'
                )
                return

        # initialize new instance
        self.logger.debug('Initializing new instance in instances list')

        instance_item = QtWidgets.QListWidgetItem(instance_name)
        self.ui.instancesList.addItem(instance_item)
        self.ui.instancesList.setCurrentItem(instance_item)

        self.logger.debug('Reset items')

        self.reset_items()
        self.ui.instanceName.setText(instance_name)

        self.logger.debug('Done')

    def remove_current_instance(self):
        """Removes current instance from the instances list (excepts the Empty only)"""

        current_instance_name = self.ui.instancesList.currentItem().text()

        if current_instance_name == 'Empty':
            return

        # remove current index item from instances list
        self.ui.instancesList.takeItem(self.ui.instancesList.row(ui.instancesList.currentItem()))

        # check for the instance in instances list
        if current_instance_name not in self.instances:
            self.warning_qmsgbox.show(
                '',
                f'Instance "{current_instance_name}" doesn\'t found to remove. '
                'Item removed from the list!'
            )
            return

        instances.pop(current_instance_name)

        # dump the instances to toml file
        save_instances_list(self.instances)

        self.information_qmsgbox.show('Success remove', f'Successfully removed the instance "{current_instance_name}"')

    def run_current_instance(self):
        """Calls the run_instance_wrapper with current instance name"""

        current_instance_name = self.ui.instancesList.currentItem().text()

        if current_instance_name == 'Empty':
            return

        self.run_instance_wrapper(current_instance_name)
