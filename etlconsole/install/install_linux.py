
import os

run_script = """
which python3
if [ $? == 1 ];
then
  echo "You didn't installed the python."
  echo "Please, install python 3.11+"
  echo "Read about it here: https://github.com/ftdot/EasyTl#setup"
  exit 1
fi
python3 easytl.py
"""

with open('run.sh', 'w') as f:
    f.write(run_script)

try:
    os.system('chmod +x run.sh')
except:
    print('Can\'t change mode of "run.sh"')