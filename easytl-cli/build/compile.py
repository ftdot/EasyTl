# must be run this script from the main directory by script "build/compile_easytl_core.py"

import py_compile
import sys
import os

# check for the arguments
if not len(sys.argv) > 1:
    raise ValueError('First argument must be path to the destination directory')

dest_dir          = sys.argv[1]
source_dir        = os.path.join(dest_dir, 'source')
source_path       = os.path.join(os.getcwd(), 'easytl-cli', 'source')


# create the dest dir
try:
    os.mkdir(dest_dir)
except FileExistsError:
    pass
except Exception as e:
    print(f'Cannot create the "{dest_dir}" directory')
    raise e


# create the core dir
try:
    os.mkdir(source_dir)
except FileExistsError:
    pass
except Exception as e:
    print('Cannot create the "source" directory')
    raise e


# compile the EasyTl-CLI core files
for f in os.listdir(source_path):
    fpath = os.path.join(source_path, f)
    py_compile.compile(fpath, cfile=os.path.join(core_dir, os.path.basename(fpath)+'c'))
