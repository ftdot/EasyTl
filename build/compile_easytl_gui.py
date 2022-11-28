# compiles the EasyTl-GUI ui's files
# must be run from main directory

import os
import traceback
from build.compile_easytl_core import run_script

build_path  = os.path.join(os.getcwd(), 'easytl-gui', 'build')
BUILD_DIR   = os.path.join(os.getcwd(), 'easytl-build')

# scripts to be executed
scripts = [
    [os.path.join(build_path, 'compile_ui.py'), []],
    [os.path.join(build_path, 'compile.py'), [BUILD_DIR, ]],
]

# create build directory
try:
    os.mkdir(BUILD_DIR)
except FileExistsError:
    print('Directory exists, skip')
except Exception as e:
    traceback.print_exception(e)
    exit(f'Can\'t create directory "{BUILD_DIR}"')


for s in scripts:
    print('Run script', *s)
    run_script(*s)
