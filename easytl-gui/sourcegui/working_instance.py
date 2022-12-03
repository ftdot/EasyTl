import os.path
import logging

from PyQt5.QtCore import QObject, pyqtSignal
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
    """

    def __init__(self, parent: QObject, instance_name: str, instance_dir: str, instance_config: dict[str, Any]):
        """
        :param parent: Parent of this QObject
        :type parent: QObject
        :param instance_name: Name of the instance
        :type instance_name: str
        :param instance_dir: Path to the directory with instance files
        :type instance_dir: str
        :param instance_config: TOML config of the instance
        :type instance_config: dict[str, Any]
        """
        super().__init__(parent)

        self.logger = logging.getLogger(f'EasyTl-GUI : WorkingInstance : {instance_name}')

        self.instance_name     = instance_name
        self.instance_dir      = instance_dir
        self.instance_config   = instance_config

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

    def initialize(self, ffmpeg_dir: str | None = None):
        """Initializes namespace objects in the EasyTl instance

        :param ffmpeg_dir: Path to the directory with ffmpeg (If is None - FFMPEG disabled)
        :type ffmpeg_dir: str | None
        """

        self.logger.debug('Initializing the instance variablies')

        if ffmpeg_dir is not None:
            self.work_instance.namespace.ffmpeg_dir = ffmpeg_dir

        self.work_instance.namespace.enable_plugins_auto_update  = self.instance_config['enable_pl_auto_update']
        self.work_instance.namespace.working_instance            = self

    def initialize_logging(self, logsEditStatus: TextEditHandler, logsEditDebug: TextEditHandler):
        """Initializes instance logging

        :param logsEditStatus: The TextEditHandler instance for logsEditStatus
        :type logsEditStatus: TextEditHandler
        :param logsEditDebug: The TextEditHandler instance for logsEditDebug
        :type logsEditDebug: TextEditHandler
        """

        self.logger.debug('Initializing the instance logging')
        try:
            # add handlers
            self.work_instance.addition_handlers.append(logsEditStatus.handler)
            self.work_instance.addition_handlers.append(logsEditDebug.handler)

            log_level = self.instance_config['logging_level']

            # initialize logging
            self.work_instance.initialize_logging(
                log_level,
                log_level if self.instance_config['console_logging_level'] == 'As logging level'
                else self.instance_config['console_logging_level']
            )
        except Exception as e:
            import traceback
            traceback.print_exception(e)

    def run(self):
        """Runs the instance"""

        self.logger.debug('Run the instance')

        # emit the signal about run
        self.logger.debug('Emitting the being run signal')
        try:

            # initialize the instance
            self.logger.debug('Initializing the instance')
            self.work_instance.initialize()

            # run the instance
            self.logger.debug('Run the instance')
            self.work_instance.run()
        except Exception as e:
            import traceback
            traceback.print_exception(e)
