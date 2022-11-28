@ECHO OFF

set PYTHONPATH=%cd%

:: compile the EasyTl
python build/compile_easytl_gui.py
python build/compile_easytl_core.py easytl-build/bin

exit