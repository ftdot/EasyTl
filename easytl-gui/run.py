import sys
import os
import subprocess

ETL_GUI_PATH  = os.getcwd()
main_path     = os.path.join(ETL_GUI_PATH, 'main.py')

# check for compiled
if not os.path.exists(main_path):
    main_path += 'c'

# add the ETL_GUI and bin folders to PYTHONPATH
os.environ['PYTHONPATH'] = (os.environ['PYTHONPATH']
                            + f';{ETL_GUI_PATH}'
                            + f';{os.path.join(ETL_GUI_PATH, "bin")}')

# run the main file
subprocess.check_call(
    [sys.executable, main_path],
    stdout=sys.stdout,
    stderr=sys.stderr,
    stdin=sys.stdin
)
