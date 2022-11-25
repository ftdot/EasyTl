# begin info
#   description = "Library-plugin | Allows to manage the commands permissions"
#   required_platforms = [ "windows", "linux", "android" ]
#   etl_version_min = [ 1, 3, 0 ]
#   etl_version_max = [ 1, 4, "*" ]
#   version = "1.3"
#   update_link = "https://github.com/ftdot/EasyTl/raw/master/plugins/SearchPlease.plugin.py"
#   lang_links = [ ["searchplease_en.toml", "https://github.com/ftdot/EasyTl/raw/master/lang/searchplease_en.toml"], ["searchplease_ru.toml", "https://github.com/ftdot/EasyTl/raw/master/lang/searchplease_ru.toml"], ["searchplease_uk.toml", "https://github.com/ftdot/EasyTl/raw/master/lang/searchplease_uk.toml"] ]
#   requirements = [ "google" ]
#   author = "ftdot (https://github.com/ftdot)"
#   changelog = [ "Added auto-update support" ]
# end info


import os
from urllib.parse import quote
from googlesearch import search as gsearch
from asyncio import sleep as async_sleep

# initialize the searchplease translations
namespace.translator.initialize('searchplease')

# the commandline to open new tab in the browser
browsers = {
    'chrome': 'chrome.exe ',
    'opera': '"C:\\Program Files (x86)\\Opera\\launcher.exe" --ran-launcher --remote ',
    'operagx': f'"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Programs\\Opera GX\\launcher.exe" --ran-launcher --remote '
}
# search engines links
search_engines = {
    'google': 'https://www.google.com/search?q=',
    'duckduckgo': 'https://www.duckduckgo.com/?q=',
    'yandex': 'https://yandex.com/search/?text='
}

# settings
find_browser     = 'operagx'     # change it to your browser
search_engine    = 'duckduckgo'  # change it to your prefer search engine
gsearch_country  = 'ua'          # "gsearch" will search in that country (write country code only!)

search_line = f'{browsers[find_browser]}{search_engines[search_engine]}'


async def unsupported_platform(event, _):
    await namespace.instance.send_unsuccess(event,
                                            namespace.translations['searchplease']['unsupported_platform'])


# opens the browser tab with the query
@this.command(namespace.translations['searchplease']['command']['search']['names'], static_pname='search')
@this.only('windows', alt=unsupported_platform)
async def search(event, args):
    if not len(args) > 0:
        return

    # Execute the commandline to open the query in the browser
    os.system(search_line + quote(' '.join(args)))
    await namespace.instance.send_success(event,
                                          namespace.translations['searchplease']['command']['search']['query_opened'])

namespace.pcommands[search.__name__].append('danger')  # mark this command as danger


# sends the results of search from the Google to the telegram chat
@this.command(namespace.translations['searchplease']['command']['gsearch']['names'])
async def gsearch_(event, args):
    if not len(args) > 0:
        return

    # if first number is numeric - type-cast it into int and use it as number of result
    num = 1
    if args[0].isnumeric():
        num = int(args[0])

    # Send query to the Google
    for url in gsearch(' '.join(args[1:]) if num > 1 else ' '.join(args), stop=num, num=num):
        await namespace.instance.send_success(
            event,
            namespace.translations['searchplease']['command']['gsearch']['link_found'].format(url)
        )
        await async_sleep(0.4)

    namespace.temp_files.append(os.path.join(namespace.instance.install_dir, '.google-cookie'))

# TODO: Support reply-search
# TODO: Image search
# TODO: Search by image
# TODO: Add browsers support: Edge, Yandex, Firefox, Tor browser
# TODO: Add support to create custom browser commandline
