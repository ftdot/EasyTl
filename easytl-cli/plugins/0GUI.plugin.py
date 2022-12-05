# begin info
#   description = "Core plugin | Basic functional for GUI"
#   required_platforms = [ "windows", "linux", "android" ]
#   required_plugins = "no requirements"
#   etl_version_min = [ 1, 4, 0 ]
#   etl_version_max = [ 1, 4, "*" ]
#   version = "1.0"
#   update_link = "https://github.com/ftdot/EasyTl/raw/master/easytl-cli/plugins/0GUI.plugin.py"
#   lang_links = [ [ "gui_en.toml", "https://github.com/ftdot/EasyTl/raw/master/easytl-cli/translations/gui_en.toml" ], [ "gui_ru.toml", "https://github.com/ftdot/EasyTl/raw/master/easytl-cli/translations/gui_ru.toml" ], [ "gui_uk.toml", "https://github.com/ftdot/EasyTl/raw/master/easytl-cli/translations/gui_uk.toml" ] ]
#   requirements = [ [ "nest-asyncio", "nest_asyncio" ]  ]
#   author = "ftdot (https://github.com/ftdot)"
# end info

import nest_asyncio
import asyncio

from source.exceptions import PluginExitedError
from PyQt5.QtCore import pyqtSlot

nest_asyncio.apply()

namespace.gui_enabled = True

# check for GUI
if not namespace.instance.config['is_gui']:
    namespace.gui_enabled = False
    this.logger.info('GUI plugin core is disabled, because instance isn\'t GUI instance')
    raise PluginExitedError(this.plugin_name)

namespace.translator.initialize('gui')

namespace.gui = namespace.Namespace()
namespace.gui.version = {
    'major': 1,
    'minor': 0,
    'patch': 2,
    'list': [1, 0, 2],
    'full_version': '1.0.2-beta'
}

####


@pyqtSlot(str)
def execute_script_line(script_line):
    this.logger.info(f'execute: {script_line}')

    try:
        exec(script_line, {n: eval(n) for n in dir()})
    except Exception as e:
        this.log_exception(e)


@pyqtSlot()
def stop():
    this.logger.info('Get stop signal from the GUI. Stopping the client')

    asyncio.get_running_loop().run_until_complete(namespace.instance.client.disconnect())


namespace.execute_script_line_signal.connect(execute_script_line)
