import os
import tomllib
import logging
import threading
import traceback
import asyncio
from PyQt5 import QtWidgets
from .window.instanceRollingWidget import Ui_instanceRollingWidget
from settings import *

from bin.source.core import Instance
from bin.source.translator import Translator

# set up the UI
InstanceRollingWidget = QtWidgets.QWidget()

ui = Ui_instanceRollingWidget()
ui.setupUi(InstanceRollingWidget)

# FUNCTIONAL

instance_dir     = None
instance_name    = None
instance_config  = None
work_instance    = None
loop             = None

is_begin_run     = False
is_run           = False

# can't initialize instance working environment
env_create_error_msgbox = QtWidgets.QMessageBox(InstanceRollingWidget)
env_create_error_msgbox.setIcon(QtWidgets.QMessageBox.Critical)
env_create_error_msgbox.setText('')
env_create_error_msgbox.setWindowTitle('Can\'t initialize environment')
env_create_error_msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok)

####

# Wrappers for the telethon


def get_phone_number():
    while 1:
        number, success = QtWidgets.QInputDialog.getText(
            InstanceRollingWidget,
            work_instance.namespace.translations['gui']['get_phone_number']['title'],
            work_instance.namespace.translations['gui']['get_phone_number']['prompt']
        )

        if success:
            break

    return number


async def get_code():
    while 1:
        code, success = QtWidgets.QInputDialog.getText(
            InstanceRollingWidget,
            work_instance.namespace.translations['gui']['get_code']['title'],
            work_instance.namespace.translations['gui']['get_code']['prompt']
        )

        if success:
            break

    return code


# wrapper for the "on_run" event
def on_run_wrapper():
    global is_run
    is_run = True
    ui.runningRatio.setChecked(is_run)

####


# initialize the instance
def initialize_instance(i_instance_name):
    global instance_dir, instance_name, instance_config, work_instance, loop

    print('initialize instance start')
    instance_name  = i_instance_name
    instance_dir   = os.path.join(INSTANCES_DIR, instance_name)

    print('check directory')
    # check for the instance directory
    if not os.path.exists(instance_dir):
        try:
            print('creating instance directory')
            # create instance directory and initializing it
            os.mkdir(instance_dir)

            from bin import initiator

            initiator.create_required_dirs(instance_dir)
            initiator.create_config_file(instance_dir)
            initiator.create_main_plugins(os.path.join(instance_dir, 'plugins'))

        except Exception as e:
            # message about the error
            env_create_error_msgbox.setText('Can\'t create environment for the instance. '
                                            f'Exception: {e}. '
                                            'Contact with the developer!')
            env_create_error_msgbox.exec_()
            return

    print('load instances')

    # load the instances list
    if os.path.exists(ALT_INSTANCES_LIST_PATH):
        with open(ALT_INSTANCES_LIST_PATH, 'rb') as f:
            instances = tomllib.load(f)
    else:
        with open(INSTANCES_LIST_PATH, 'rb') as f:
            instances = tomllib.load(f)

    # get config of the instance
    instance_config = instances[instance_name]

    # create instance
    work_instance = Instance(
        instance_name,
        instance_config['api_id'],
        instance_config['api_hash'],
        [int(instance_config['owner_id']), ],
        os.path.join(instance_dir, 'config.toml'),
        Translator(os.path.join(instance_dir, 'translations')),
        instance_dir,
        os.path.join(instance_dir, 'plugins'),
        os.path.join(instance_dir, 'cache'),
        os.path.join(instance_dir, 'logs')
    )

    print('initialize logging')

    # initialize logging
    log_level = getattr(logging, instance_config['logging_level'])

    work_instance.initialize_logging(
        log_level,
        log_level if instance_config['console_logging_level'] == 'As logging level'
        else getattr(logging, instance_config['console_logging_level'])
    )

    # set up namespace variables
    work_instance.namespace.ffmpeg_dir = os.path.join(os.getcwd(), 'ffmpeg', 'ffmpeg-master-latest-win64-gpl-shared')
    work_instance.namespace.instance_file = os.path.abspath(__file__)
    work_instance.namespace.enable_plugins_auto_update = instance_config['enable_pl_auto_update']

    # set up wrappers to get values to authorize
    work_instance._t_get_phone = get_phone_number
    work_instance._t_get_code = get_code

    # set up on_run event
    work_instance.namespace.on_run = on_run_wrapper

    ui.groupBox.setTitle(instance_name)


def run_work_instance():
    global is_begin_run

    if work_instance is None or is_begin_run:
        return

    is_begin_run = True

    try:
        def run_instance():
            global loop

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            # initialize the instance and run it
            work_instance.initialize()
            work_instance.run()

        threading.Thread(target=run_instance).start()
    except Exception as e:
        traceback.print_exception(e)


ui.runningRatio.toggled.connect(lambda: ui.runningRatio.setChecked(is_run))
ui.startBtn.clicked.connect(run_work_instance)
