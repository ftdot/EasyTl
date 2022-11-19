import sys
import os
import traceback
from zipfile import ZipFile

if sys.platform.startswith('linux'):
    print('Installing ffmpeg with APT')

    try:
        os.system('apt install ffmpeg')

    except IOError as e:
        sys.exit('Can\'t install the ffmpeg')

elif sys.platform == 'win32':
    print('extract the ffmpeg')
    try:
        os.mkdir('ffmpeg')
        with ZipFile(os.path.join('install', 'ffmpeg-win32.zip')) as zf:
            zf.extractall('ffmpeg')

        print('Install successful!')
    except Exception as e:
        traceback.print_exception(e)
        sys.exit('Can\'t install the ffmpeg')

else:
    sys.exit('This platform isn\'t supported')
