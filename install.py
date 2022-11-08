import sys
import logging
import os
import time
import traceback
import subprocess

# advanced settings
requirements_file  = 'requirements.txt'

log_level          = logging.DEBUG
file_log_level     = logging.DEBUG
logs_dir           = os.path.join(os.getcwd(), 'logs')


#####

# formatter for the logger
s_format = '%(name)s | %(asctime)s | [%(levelname)s] : %(message)s'
formatter = logging.Formatter(s_format)

# configuring the logging
logging.basicConfig(
    format=s_format, datefmt='%H:%M:%S',
    filename=os.path.join(logs_dir,
                          f'INSTALLER-{time.strftime("%Y-%m-%d_%H-%M", time.localtime())}-log.txt'),
    level=file_log_level
)

# setup the logger
logger = logging.Logger('Installer')

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(log_level)
handler.setFormatter(formatter)
logger.addHandler(handler)

#####

logger.info('Installing is begin')

# check for the python version
if sys.version_info.minor < 11:
    logger.info('Minimum python required: Python 11')
    logger.info('You can get it from the official site: https://www.python.org/')

    logger.debug('Incorrect python version, exiting')
    exit()

# install the requirements
logging.debug('Installing the requirements')

try:
    logger.info('Installing the required packages')
    # run PIP to install the package
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_file])

except Exception as e:
    logger.debug('#' * 25)

    logger.error('Exception has been generated, while executing the command')
    for line in traceback.format_exception(e):
        logger.debug(line.removesuffix('\n'))

    logger.debug('#' * 25)

logging.info('All done, you can sleep peacefully')
