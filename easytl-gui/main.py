import sys
import traceback
from PyQt5 import QtWidgets, QtGui
from qt_material import apply_stylesheet as qtm_apply_style
from settings import *

# initialize the app
app = QtWidgets.QApplication(sys.argv)
qtm_apply_style(app, theme='dark_cyan.xml')

# app
from gui import instance_settings_widget
from gui import instance_rolling_widget

main_window = QtWidgets.QMainWindow()
main_window.setWindowTitle("EasyTl | Instances")
main_window.setWindowIcon(QtGui.QIcon(ICON_PATH))


# wrapper for the run instance
def run_instance_wrapper_(instance_name):
    print('wrapper called')
    instance_settings_widget.InstanceSettingsWidget.destroy(False, False)

    print('set widgets')
    main_window.setWindowTitle(f"EasyTl | {instance_name}")
    main_window.setCentralWidget(instance_rolling_widget.InstanceRollingWidget)

    print('initialize instance')
    instance_rolling_widget.initialize_instance(instance_name)
instance_settings_widget.run_instance_wrapper = run_instance_wrapper_

main_window.setCentralWidget(instance_settings_widget.InstanceSettingsWidget)
main_window.show()

app.exec_()
