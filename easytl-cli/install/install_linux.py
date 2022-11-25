
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

with open('run.sh') as f:
    f.write(run_script)
