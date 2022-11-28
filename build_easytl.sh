export PYTHONPATH=%cd%

# compile the EasyTl
python3 build/compile_easytl_gui.py
python3 build/compile_easytl_core.py easytl-build/bin
