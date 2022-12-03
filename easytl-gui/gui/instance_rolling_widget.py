import os
import logging
import threading

from PyQt5 import QtWidgets
from PyQt5 import QtCore

from .window.instanceRollingWidget import Ui_instanceRollingWidget
from settings import *

from sourcegui.texteditlogging import TextEditHandler
from sourcegui.working_instance import WorkingInstance
from sourcegui.utils import QuickMessageBox, load_instances_list

from bin import initiator


class InstanceRollingWidget(QtWidgets.QWidget):
    """Functional defines for Instance Rolling UI

    :ivar instances: Dict with the instances
    :type instances: dict[str, Any]
    :ivar working_instance: Current working instance
    :type working_instance: WorkingInstance
    :ivar instance_thread: Thread for the EasyTl instance
    :type instance_thread: QtCore.QThread
    :ivar ui: Ui_instanceRollingWidget instance
    :type ui: Ui_instanceRollingWidget
    :ivar logsEditStatus_handler: TextEditHandler instance for ui.logsEditStatus
    :type logsEditStatus_handler: TextEditHandler
    :ivar logsEditDebug_handler: TextEditHandler instance for ui.logsEditStatus
    :type logsEditDebug_handler: TextEditHandler
    :ivar is_run: Indicates if instance is running
    :type is_run: bool
    :ivar critical_qmsgbox: QuickMessageBox instance with Critical icon and Ok button
    :type critical_qmsgbox: QuickMessageBox
    """

    def __init__(self, parent: QtCore.QObject):
        """
        :param parent: Parent of the widget
        :type parent: QtCore.QObject
        """
        super().__init__(parent)

        self.logger = logging.getLogger('EasyTl-GUI : InstanceRollingWidget')

        self.instances         = {}
        self.working_instance  = None
        self.instance_thread   = QtCore.QThread()

        self.ui                      = None
        self.logsEditStatus_handler  = None
        self.logsEditDebug_handler   = None

        self.is_run = False

        self.critical_qmsgbox = QuickMessageBox(self, QtWidgets.QMessageBox.Critical, QtWidgets.QMessageBox.Ok)

    def initialize(self):
        """Initializes the widget"""

        self.logger.debug('Initializing the UI')

        # set up UI
        self.ui = Ui_instanceRollingWidget()
        self.ui.setupUi(self)

        self.logger.debug('Initializing the buttons')

        # initialize the buttons
        self.ui.startBtn.setProperty('class', 'success')
        self.ui.stopBtn.setProperty('class', 'danger')
        self.ui.restartBtn.setProperty('class', 'warning')

        self.logger.debug('Initializing the connections')

        # initialize connections
        self.ui.runningRatio.toggled.connect(lambda: self.ui.runningRatio.setChecked(self.is_run))
        self.ui.startBtn.clicked.connect(self.run_working_instance)

    ####

    def get_phone_number(self) -> str:
        """(For EasyTl instance) Gets the phone number prompt from user

        :returns: The phone number, entered by user
        :rtype: str
        """

        self.logger.debug('Getting the phone number')

        while 1:
            number, success = QtWidgets.QInputDialog.getText(
                self,
                self.working_instance.namespace.translations['gui']['get_phone_number']['title'],
                self.working_instance.namespace.translations['gui']['get_phone_number']['prompt']
            )

            if success:
                break

        return number

    async def get_code(self) -> str:
        """(For EasyTl instance) Gets the auth code prompt from user

        :returns: The auth code, entered by user
        :rtype: str
        """

        self.logger.debug('Getting the auth code')

        while 1:
            code, success = QtWidgets.QInputDialog.getText(
                self,
                self.working_instance.namespace.translations['gui']['get_code']['title'],
                self.working_instance.namespace.translations['gui']['get_code']['prompt']
            )

            if success:
                break

        return code

    def on_run_wrapper(self):
        """(System) Calls it when instance is run"""
        self.is_run = True
        self.ui.runningRatio.setChecked(self.is_run)

    ####

    def check_environment(self, instance_dir: str):
        """Checks/Create the environment in the instance directory

        :param instance_dir: Path to the instance environment directory
        :type instance_dir: str
        """

        if not os.path.exists(instance_dir):
            try:
                # create instance directory and initializing it
                os.mkdir(instance_dir)

                self.logger.debug('Create the required directories')
                initiator.create_required_dirs(instance_dir)

                self.logger.debug('Create the config file')
                initiator.create_config_file(instance_dir)

                self.logger.debug('Create the main plugins')
                initiator.create_main_plugins(os.path.join(instance_dir, 'plugins'))

            except Exception as e:
                # TODO: pluginapi.Plugin.log_exception -> utils.log_exception

                # message about the error
                self.critical_qmsgbox.show('Environment checking error',
                                           'While checking\\creating the environment for the instance')
    ####

    def initialize_instance(self, instance_name: str):
        """Initializes the instance

        :param instance_name: Name of the instance (must be in instances_dir/list.toml file)
        :type instance_name: str
        """

        self.logger.debug(f'Initializing instance "{instance_name}"')

        instance_dir     = os.path.join(INSTANCES_DIR, instance_name)
        instance_config  = load_instances_list()[instance_name]

        self.check_environment(instance_dir)

        self.logger.debug('Creating WorkingInstance')
        self.working_instance = WorkingInstance(self, instance_name, instance_dir, instance_config)

        self.logger.debug('Initializing WorkingInstance')
        self.working_instance.initialize(os.path.join(os.getcwd(), 'ffmpeg', 'ffmpeg-master-latest-win64-gpl-shared'))
        self.working_instance.work_instance.namespace.on_run = self.on_run_wrapper

        self.ui.groupBox.setTitle(instance_name)

        self.logger.debug('Initialized success')

        # set up the logsEditStatus handler
        self.logger.debug('Creating TextEditHandler for the logsEditStatus')
        self.logsEditStatus_handler = TextEditHandler()
        self.logsEditStatus_handler.initialize(self.working_instance.instance_config['logging_level'])
        self.logsEditStatus_handler.flush_signal.connect(self.write_buffer_logsEditStatus)

        # set up the logsEditDebug handler
        self.logger.debug('Creating TextEditHandler for the logsEditDebug')
        self.logsEditDebug_handler = TextEditHandler()
        self.logsEditDebug_handler.initialize(logging.DEBUG)
        self.logsEditDebug_handler.flush_signal.connect(self.write_buffer_logsEditDebug)

        # move to the thread these
        self.logger.debug('Initializing the instance thread')
        self.logsEditStatus_handler.moveToThread(self.instance_thread)
        self.logsEditDebug_handler.moveToThread(self.instance_thread)
        self.working_instance.moveToThread(self.instance_thread)

        # add the thread started connections
        self.instance_thread.started.connect(self.working_instance.run)

        # initialize logging
        self.logger.debug('Initializing WorkingInstance logging')
        self.working_instance.initialize_logging(self.logsEditStatus_handler, self.logsEditDebug_handler)

        self.logger.debug('Instance initializing done')

    def run_working_instance(self):
        """Runs the current WorkingInstance"""

        self.logger.info('Run the instance')

        self.logger.debug('Run the instance thread')

        # run thread
        self.instance_thread.start()

    ####

    @QtCore.pyqtSlot()
    def write_buffer_logsEditStatus(self):
        """(System) Writes the handler buffer to logsEditStatus"""
        self.logger.debug('Write logsEditStatus buffer')
        self.ui.logsEditStatus.setText(self.ui.logsEditStatus.toPlainText() + self.logsEditStatus_handler.buffer)
        self.logsEditStatus_handler.clear_signal.emit()

    @QtCore.pyqtSlot()
    def write_buffer_logsEditDebug(self):
        """(System) Writes the handler buffer to logsEditDebug"""
        self.logger.debug('Write logsEditDebug buffer')
        self.ui.logsEditDebug.setText(self.ui.logsEditDebug.toPlainText() + self.logsEditDebug_handler.buffer)
        self.logsEditDebug_handler.clear_signal.emit()
