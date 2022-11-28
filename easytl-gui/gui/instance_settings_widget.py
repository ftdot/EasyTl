import os
import sys
import tomllib
import toml
import subprocess
import threading
from PyQt5 import QtWidgets
from .window.instanceSettingsWidget import Ui_instanceSettingsWidget
from settings import *

# set up the UI
InstanceSettingsWidget = QtWidgets.QWidget()

ui = Ui_instanceSettingsWidget()
ui.setupUi(InstanceSettingsWidget)

# FUNCTIONAL

instances                = {}
allowed_instances_chars  = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890_'
run_instance_wrapper     = lambda _: None

# variables to save [config_name] = [eval_value]
save_vars_dict = {
    'api_id': 'ui.apiIdEdit.text()',
    'api_hash': 'ui.apiHashEdit.text()',
    'owner_id': 'ui.ownerIdEdit.text()',

    'enable_pl_auto_update': 'ui.enablePLAutoUpdateChB.isChecked()',
    'logging_level': 'ui.loggingLevelCB.currentText()',
    'console_logging_level': 'ui.consoleLoggingLevelCB.currentText()'
}


# disallowed characters message box
disallowed_chars_msgbox = QtWidgets.QMessageBox(InstanceSettingsWidget)
disallowed_chars_msgbox.setIcon(QtWidgets.QMessageBox.Warning)
disallowed_chars_msgbox.setText('')
disallowed_chars_msgbox.setWindowTitle('Incorrect Instance name')
disallowed_chars_msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok)

# instance not found message box
instance_not_found_msgbox = QtWidgets.QMessageBox(InstanceSettingsWidget)
instance_not_found_msgbox.setIcon(QtWidgets.QMessageBox.Critical)
instance_not_found_msgbox.setText('')
instance_not_found_msgbox.setWindowTitle('Instance not found')
instance_not_found_msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok)

# success save message (also success remove instance message)
success_save_msgbox = QtWidgets.QMessageBox(InstanceSettingsWidget)

success_save_msgbox.setIcon(QtWidgets.QMessageBox.Information)
success_save_msgbox.setText('')
success_save_msgbox.setWindowTitle('Success')
success_save_msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok)


# resets the GUI items
def reset_items():
    ui.instanceName.setText('No instance')
    ui.apiIdEdit.setText('')
    ui.apiHashEdit.setText('')
    ui.ownerIdEdit.setText('')

    ui.enablePLAutoUpdateChB.setChecked(True)
    ui.loggingLevelCB.setCurrentText('INFO')
    ui.consoleLoggingLevelCB.setCurrentText('As logging level')


# loads instances variable + adds instances to instances list (gui)
def initialize_instances():
    global instances

    # load the instances list
    if os.path.exists(ALT_INSTANCES_LIST_PATH):
        with open(ALT_INSTANCES_LIST_PATH, 'rb') as f:
            instances = tomllib.load(f)
    else:
        with open(INSTANCES_LIST_PATH, 'rb') as f:
            instances = tomllib.load(f)

    for instance_name in instances.keys():
        ui.instancesList.addItem(QtWidgets.QListWidgetItem(instance_name))


# loads the instance settings
def load_instance_settings(instance_name):
    if instance_name == 'Empty':
        ui.instanceName.setText('Empty instance (can\'t to be saved and used!)')
        return
    ui.instanceName.setText(instance_name)

    if instance_name not in instances:
        return

    ui.apiIdEdit.setText(instances[instance_name]['api_id'])
    ui.apiHashEdit.setText(instances[instance_name]['api_hash'])
    ui.ownerIdEdit.setText(instances[instance_name]['owner_id'])

    ui.enablePLAutoUpdateChB.setChecked(instances[instance_name]['enable_pl_auto_update'])
    ui.loggingLevelCB.setCurrentText(instances[instance_name]['logging_level'])
    ui.consoleLoggingLevelCB.setCurrentText(instances[instance_name]['console_logging_level'])


# saves the instance settings
def save_instance_settings():
    current_instance_name = ui.instancesList.currentItem().text()

    if current_instance_name == 'Empty':
        return

    # check for the disallowed characters
    for char in current_instance_name:
        if char not in allowed_instances_chars:
            disallowed_chars_msgbox.setText(
                f'Name "{current_instance_name}" is incorrect, because contains disallowed characters. '
                'Instance isn\'t saved!'
            )
            disallowed_chars_msgbox.exec_()
            return

    # check for the api id, owner id
    if not ui.ownerIdEdit.text().isnumeric():
        disallowed_chars_msgbox.setText(
            f'Owner ID value is incorrect, because contains disallowed characters. '
            'Instance isn\'t saved!'
        )
        disallowed_chars_msgbox.exec_()
        return

    if not ui.apiIdEdit.text().isnumeric():
        disallowed_chars_msgbox.setText(
            f'API ID value is incorrect, because contains disallowed characters. '
            'Instance isn\'t saved!'
        )
        disallowed_chars_msgbox.exec_()
        return

    # check for the new instance
    if current_instance_name not in instances:
        instances[current_instance_name] = {}

    # set all config values
    for config_value, eval_value in save_vars_dict.items():
        instances[current_instance_name][config_value] = eval(eval_value)

    # dump the instances to toml file
    if os.path.exists(ALT_INSTANCES_LIST_PATH):
        with open(ALT_INSTANCES_LIST_PATH, 'w') as f:
            toml.dump(f)
    else:
        with open(INSTANCES_LIST_PATH, 'w') as f:
            toml.dump(f)

    # create message of success save
    success_save_msgbox.setText(f'Instance "{current_instance_name}" successfully saved!')
    success_save_msgbox.exec_()


# creates new instance (in the list only, to have "save_instance_settings" function)
def create_new_instance():
    instance_name, success = QtWidgets.QInputDialog.getText(
        InstanceSettingsWidget,
        'New instance',
        'Enter new instance name:'
    )

    if not success:
        return

    # check for the disallowed characters
    for char in instance_name:
        if char not in allowed_instances_chars:
            disallowed_chars_msgbox.setWindowTitle(
                f'Name "{instance_name}" is incorrect, because contains disallowed characters. '
                'Instance isn\'t saved!'
            )
            disallowed_chars_msgbox.exec_()
            return

    # initialize new instance

    instance_item = QtWidgets.QListWidgetItem(instance_name)
    ui.instancesList.addItem(instance_item)
    ui.instancesList.setCurrentItem(instance_item)

    reset_items()

    ui.instanceName.setText(instance_name)


# removes current instance
def remove_current_instance():
    current_instance_name = ui.instancesList.currentItem().text()

    if current_instance_name == 'Empty':
        return

    idx = ui.instancesList.row(ui.instancesList.currentItem())

    ui.instancesList.takeItem(idx)

    # check for the instance in instances list
    if current_instance_name not in instances:
        instance_not_found_msgbox.setText(f'Instance "{current_instance_name}" doesn\'t found to remove. '
                                                 'Item removed from the list!')
        instance_not_found_msgbox.exec_()
        return

    instances.pop(current_instance_name)

    # dump the instances to toml file
    if os.path.exists(ALT_INSTANCES_LIST_PATH):
        with open(ALT_INSTANCES_LIST_PATH, 'w') as f:
            toml.dump(f)
    else:
        with open(INSTANCES_LIST_PATH, 'w') as f:
            toml.dump(f)

    success_save_msgbox.setText(f'Successfully removed the instance "{current_instance_name}"')
    success_save_msgbox.exec_()


# run instance
def run_current_instance():
    current_instance_name = ui.instancesList.currentItem().text()

    if current_instance_name == 'Empty':
        return

    run_instance_wrapper(current_instance_name)

####

reset_items()

ui.instancesList.addItem(QtWidgets.QListWidgetItem('Empty'))
initialize_instances()

# add functional to ui
ui.instancesList.currentItemChanged.connect(lambda: load_instance_settings(ui.instancesList.currentItem().text()))
ui.saveSettingsButton.clicked.connect(save_instance_settings)
ui.newInstanceButton.clicked.connect(create_new_instance)
ui.removeInstanceButton.clicked.connect(remove_current_instance)
ui.runInstanceButton.clicked.connect(run_current_instance)
