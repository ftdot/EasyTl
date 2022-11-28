# must be run this script from the main directory by script "build/compile_easytl_gui_ui.py"
import os
import sys
import subprocess
import traceback

ETL_GUI_DIR  = os.path.join(os.getcwd(), 'easytl-gui')
UI_DIR       = os.path.join(ETL_GUI_DIR, 'ui')

uis_to_compile = [
    [os.path.join(UI_DIR, 'instanceSettingsWidget.ui'), os.path.join(ETL_GUI_DIR, 'gui', 'window', 'instanceSettingsWidget.py')],
    [os.path.join(UI_DIR, 'instanceRollingWidget.ui'), os.path.join(ETL_GUI_DIR, 'gui', 'window', 'instanceRollingWidget.py')]
]


def call_command(cmdline, args):
    try:
        # run PIP to install the package
        subprocess.check_call(
            [sys.executable, cmdline, ] + args,
            stdout=sys.stdout,
            stderr=sys.stdout
        )
    except Exception as e:
        print(f'While running command "{cmdline} {args}" occurred the error:')
        traceback.print_exception(e)
        exit('Command returned error')

for ui in uis_to_compile:
    print(f'Compile UI: {ui[0]} -> {ui[1]}')
    call_command('-m', ['PyQt5.uic.pyuic', f'-o{ui[1]}', ui[0]])
