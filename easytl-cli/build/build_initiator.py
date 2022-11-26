# must be run this script from the main directory by script "build/compile_easytl_core.py"

import sys
import os
import py_compile

# check for the arguments
if not len(sys.argv) > 1:
    raise ValueError('First argument must be path to the output file path')

dest_path       = sys.argv[1]
dest_file       = os.path.join(dest_path, 'initiator.pyc')
initiator_path  = os.path.join(os.getcwd(), 'easytl-cli', 'build', 'initiator.py')


# save the config
with open(os.path.join(os.getcwd(), 'easytl-cli', 'config.toml')) as f:
    config_toml = f.read()

# copy the initiator file
with open(dest_file+'_tmp.py', 'w') as f1:
    with open(initiator_path, 'r') as f2:
        f1.write(f2.read().replace('{{ CONFIG_TOML }}', config_toml))

# compile the file
py_compile.compile(dest_file+'_tmp.py', cfile=dest_file)

# try to remove temp file
try:
    os.remove(dest_file+'_tmp.py')
except PermissionError:
    exit('Can\'t remove temp file')
