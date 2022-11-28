# must be run this script from the main directory by script "build/compile_easytl_gui.py"
import os
import sys
import subprocess
import traceback
import py_compile

dest_dir          = sys.argv[1]
ETL_GUI_DIR       = os.path.join(os.getcwd(), 'easytl-gui')

files_to_compile = [
    os.path.join('gui', 'instance_settings_widget.py'),
    os.path.join('gui', 'instance_rolling_widget.py'),
    os.path.join('gui', 'window', 'instanceSettingsWidget.py'),
    os.path.join('gui', 'window', 'instanceRollingWidget.py'),
    os.path.join('main.py'),
    os.path.join('run.py'),
    os.path.join('settings.py')
]

files_to_create = [
    os.path.join(dest_dir, 'instances', 'list.toml')
]

dirs_to_create = [
    os.path.join(dest_dir, 'bin'),
    os.path.join(dest_dir, 'gui'),
    os.path.join(dest_dir, 'gui', 'window'),
    os.path.join(dest_dir, 'instances'),
    os.path.join(dest_dir, 'resources')
]


# create required directories
for dir_ in dirs_to_create:
    try:
        print(f'Creating directory {dir_}')
        os.mkdir(dir_)
    except FileExistsError:
        print('Directory exists, skip')
    except Exception as e:
        traceback.print_exception(e)
        exit('Can\'t create directory')

# create required files
for f in files_to_create:
    print('Creating file:', f)
    with open(f, 'w'):
        pass

# compile the EasyTl-GUI files
for f in files_to_compile:
    py_compile.compile(os.path.join(ETL_GUI_DIR, f), cfile=os.path.join(dest_dir, f+'c'))
