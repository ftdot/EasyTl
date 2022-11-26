
import os

required_dirs = [
    'cache',
    'logs',
    'plugins',
    'translations'
]

config_toml = '''{{ CONFIG_TOML }}'''


# creates required directories in instance directory
def create_required_dirs(instance_dir):
    for dir_ in required_dirs:
        os.mkdir(os.path.join(instance_dir, dir_))


# creates config file
def create_config_file(path):
    with open(path, 'w') as f:
        f.write(config_toml)