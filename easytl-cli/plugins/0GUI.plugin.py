# begin info
#   description = "Core plugin | Basic functional for GUI"
#   required_platforms = [ "windows", "linux", "android" ]
#   required_plugins = "no requirements"
#   etl_version_min = [ 1, 4, 0 ]
#   etl_version_max = [ 1, 4, "*" ]
#   version = "1.0"
#   update_link = "https://github.com/ftdot/EasyTl/raw/master/easytl-cli/plugins/0GUI.plugin.py"
#   lang_links = [ [ "gui_en.toml", "https://github.com/ftdot/EasyTl/raw/master/easytl-cli/translations/gui_en.toml" ], [ "gui_ru.toml", "https://github.com/ftdot/EasyTl/raw/master/easytl-cli/translations/gui_ru.toml" ], [ "gui_uk.toml", "https://github.com/ftdot/EasyTl/raw/master/easytl-cli/translations/gui_uk.toml" ] ]
#   requirements = "no requirements"
#   author = "ftdot (https://github.com/ftdot)"
# end info

from source.exceptions import PluginExitedError

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
    'patch': 1,
    'list': [1, 0, 1],
    'full_version': '1.0.1-beta'
}
