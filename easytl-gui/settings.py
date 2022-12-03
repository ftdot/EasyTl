import os

# settings
RESOURCES_DIR  = os.path.join(os.getcwd(), 'resources')
INSTANCES_DIR  = os.path.join(os.getcwd(), 'instances')
BIN_DIR        = os.path.join(os.getcwd(), 'bin')
LOGS_DIR       = os.path.join(os.getcwd(), 'logs')

EASYTL_CLI_WORKER        = os.path.join(BIN_DIR, 'instance_worker.py')
ICON_PATH                = os.path.join(RESOURCES_DIR, 'icon.png')
INSTANCES_LIST_PATH      = os.path.join(INSTANCES_DIR, 'list.toml')  # do not change it
ALT_INSTANCES_LIST_PATH  = os.path.join(INSTANCES_DIR, 'alt_list.toml')

LOG_LEVEL         = 'DEBUG'
STDOUT_LOG_LEVEL  = 'DEBUG'
FILE_LOG_LEVEL    = 'DEBUG'
