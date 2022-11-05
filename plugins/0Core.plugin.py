# description := Core plugin | Basic functional
# required_platforms := windows, linux, android
# etl_version := 0
# version := 1.0
# update_link := no-link
# lang_links := no-links
# requirements := no-requirements
# author := ftdot (https://github.com/ftdot)

def cyrillic(string: str):
    """Fixes cyrillic encoding problem

    :returns: Encoded string with UTF-8
    """

    return string.encode('1251').decode('utf8')

namespace.cyrillic = cyrillic

# initialize the default translations
namespace.translator.initialize('core')
namespace.translator.initialize('builtin_libs')

# get the prefixes
namespace.instance.prefixes = namespace.translator.get('core.core.prefixes')
