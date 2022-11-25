
run_script = """
@ECHO OFF
setlocal

python -V >nul
if not errorlevel 0 goto no_python
goto run_install

:no_python
echo.
echo At this computer doesn't installed the python.
echo Install the python before installing the EasyTl
echo Read about it here: https://github.com/ftdot/EasyTl#setup
echo.
pause
exit

:run_install
python easytl.py
PAUSE
exit
"""

with open('run.bat') as f:
    f.write(run_script)
