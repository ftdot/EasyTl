import sys
import time
import traceback
import logging

from PyQt5 import QtWidgets, QtGui
from qt_material import apply_stylesheet as qtm_apply_style

from settings import *

# initialize the app
app = QtWidgets.QApplication(sys.argv)
qtm_apply_style(app, theme='dark_cyan.xml')

# logging

# format
log_format = '%(name)s | %(asctime)s | [%(levelname)s] : %(message)s'
formatter = logging.Formatter(log_format)

# set up console handler
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(STDOUT_LOG_LEVEL)
stdout_handler.setFormatter(formatter)

# set up file handler
file_handler = logging.StreamHandler(
    open(os.path.join(LOGS_DIR, f'{time.strftime("%Y-%m-%d_%H-%M", time.localtime())}-log.txt'), 'w')
)
file_handler.setLevel(FILE_LOG_LEVEL)
file_handler.setFormatter(formatter)

# configure the logging
logging.basicConfig(
    format=log_format, datefmt='%H:%M:%S',
    level=LOG_LEVEL,
    handlers=[stdout_handler, file_handler]
)

logger = logging.getLogger('EasyTl-GUI : Main')
logger.info('Logging is initialized')

# app
from gui import instance_settings_widget
from gui import instance_rolling_widget

logger.debug('Initializing the main window')

main_window = QtWidgets.QMainWindow()
main_window.setWindowTitle("EasyTl | Instances")
main_window.setWindowIcon(QtGui.QIcon(ICON_PATH))

logger.debug('Creating instance of InstanceSettingsWidget')

# InstanceSettingsWidget
ISW = instance_settings_widget.InstanceSettingsWidget(main_window)
ISW.initialize()

logger.debug('Creating instance of InstanceRollingWidget')

# InstanceRollingWidget
IRW = instance_rolling_widget.InstanceRollingWidget(main_window)
IRW.initialize()
IRW.hide()


# wrapper for the run instance
def run_instance_wrapper_(instance_name):
    ISW.destroy(False, False)
    IRW.show()

    main_window.setWindowTitle(f"EasyTl | {instance_name}")
    main_window.setCentralWidget(IRW)

    IRW.initialize_instance(instance_name)
ISW.run_instance_wrapper = run_instance_wrapper_

logger.debug('Set central widget -> ISW')

main_window.setCentralWidget(ISW)
main_window.show()

logger.debug('Executing the application')

app.exec_()
