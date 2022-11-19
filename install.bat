@ECHO OFF
setlocal
;;set "[[=>"#" 2>&1&set/p "&set "]]==<# & del /q # >nul 2>&1" &

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
python install\install.py
PAUSE
exit