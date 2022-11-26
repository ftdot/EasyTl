
import os

required_dirs = [
    'cache',
    'logs',
    'plugins',
    'translations'
]

config_toml   = r'''{{ CONFIG_TOML }}'''
core_plugin   = r'''{{ CORE_PLUGIN }}
# MUST BE UPDATED'''
perms_plugin  = r'''{{ PERMS_PLUGIN }}
# MUST BE UPDATED'''


# creates required directories in instance directory
def create_required_dirs(instance_dir):
    for dir_ in required_dirs:
        os.mkdir(os.path.join(instance_dir, dir_))


# creates config file
def create_config_file(path):
    with open(path, 'w') as f:
        f.write(config_toml)


# create main plugins
def create_main_plugins(plugins_dir):
    with open(os.path.join(plugins_dir, '0Core.plugin.py'), 'w') as f:
        f.write(core_plugin)
    with open(os.path.join(plugins_dir, '0Permissions.plugin.py'), 'w') as f:
        f.write(perms_plugin)
