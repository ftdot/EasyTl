import os.path
import logging
import asyncio

from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from typing import Any

from bin.source.core import Instance
from bin.source.translator import Translator

from sourcegui.texteditlogging import TextEditHandler


class WorkingInstance(QObject):
    """Class helps run EasyTl instance


    :ivar instance_name: Name of the instance
    :type instance_name: str
    :ivar instance_dir: Path to the instance environment directory
    :type instance_dir: str
    :ivar instance_config: Config of the instance
    :type instance_config: dict[str, Any]
    :ivar addition_handlers: List with the instance logger addition handlers
    :type addition_handlers: list
    :ivar qthread: QThread instance for run the EasyTl instance
    :type qthread: QThread
    :ivar execute_script_line_signal: PyQT signal for executing script line in DEBUG tab
    :type execute_script_line_signal: pyqtSignal
    """
    execute_script_line_signal = pyqtSignal(str, name='ExecScriptLineSignal')

    def __init__(self, instance_name: str, instance_dir: str, instance_config: dict[str, Any]):
        """
        :param instance_name: Name of the instance
        :type instance_name: str
        :param instance_dir: Path to the directory with instance files
        :type instance_dir: str
        :param instance_config: TOML config of the instance
        :type instance_config: dict[str, Any]
        """
        super().__init__()

        self.logger = logging.getLogger(f'EasyTl-GUI : WorkingInstance : {instance_name}')

        self.instance_name      = instance_name
        self.instance_dir       = instance_dir
        self.instance_config    = instance_config

        self.addition_handlers  = []
        self.qthread            = QThread()

        # create instance
        self.work_instance = Instance(
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

    def initialize(self, ffmpeg_dir: str | None = None, addition_handlers: list | None = None):
        """Initializes namespace objects in the EasyTl instance

        :param ffmpeg_dir: Path to the directory with ffmpeg (If is None - FFMPEG disabled)
        :type ffmpeg_dir: str | None
        :param addition_handlers: List with the addition handlers
        :type addition_handlers: list
        """

        self.logger.debug('Initializing the instance variables')

        # check for ffmpeg
        if ffmpeg_dir is not None:
            self.work_instance.namespace.ffmpeg_dir = ffmpeg_dir

        self.work_instance.namespace.enable_plugins_auto_update  = self.instance_config['enable_pl_auto_update']
        self.work_instance.namespace.working_instance            = self

        # signals for the GUI
        self.work_instance.namespace.execute_script_line_signal  = self.execute_script_line_signal

        self.logger.debug('Adding the addition handlers to the qthread')

        # check for addition handlers
        if addition_handlers is not None:
            for ah in addition_handlers:
                self.addition_handlers.append(ah.handler)
                ah.moveToThread(self.qthread)

        self.logger.debug('Initializing qthread')

        # initialize thread
        self.moveToThread(self.qthread)
        self.qthread.started.connect(self._run)

    def initialize_logging(self):
        """Initializes instance logging"""

        self.logger.debug('Initializing the instance logging')

        # add handlers
        self.work_instance.addition_handlers += self.addition_handlers

        log_level = self.instance_config['logging_level']

        # initialize logging
        self.work_instance.initialize_logging(
            log_level,
            log_level if self.instance_config['console_logging_level'] == 'As logging level'
            else self.instance_config['console_logging_level']
        )

    @pyqtSlot()
    def _run(self):

        # initialize asyncio event loop
        self.logger.debug('Initializing asyncio event loop')
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # initialize the logging
        self.initialize_logging()

        # initialize the instance
        self.logger.debug('Initializing the instance')
        self.work_instance.initialize()

        # run the instance
        self.logger.debug('Run the instance')
        self.work_instance.run()

    def run(self):
        """Runs the instance"""

        self.logger.info('Running the thread')
        self.qthread.start()
