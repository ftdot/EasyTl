# begin info
#   description = "Library-plugin | Allows to manage the commands permissions"
#   required_platforms = [ "windows", "linux", "android" ]
#   etl_version_min = [ 1, 4, 0 ]
#   etl_version_max = [ 1, 4, "*" ]
#   version = "1.5"
#   update_link = "https://github.com/ftdot/EasyTl/raw/master/easytl-cli/plugins/SearchPlease.plugin.py"
#   lang_links = [ ["searchplease_en.toml", "https://github.com/ftdot/EasyTl/raw/master/easytl-cli/translations/searchplease_en.toml"], ["searchplease_ru.toml", "https://github.com/ftdot/EasyTl/raw/master/easytl-cli/translations/searchplease_ru.toml"], ["searchplease_uk.toml", "https://github.com/ftdot/EasyTl/raw/master/easytl-cli/translations/searchplease_uk.toml"] ]
#   requirements = [ "google", "BeautifulSoup4" ]
#   author = "ftdot (https://github.com/ftdot)"
#   changelog = [ "Added search images by query", "Added Edge, FireFox, Default browsers support", "Reply search support for the gsearch, gimgsearch commands" ]
# end info


import os
import re
from urllib import request
from urllib.parse import quote
from googlesearch import search as gsearch
from asyncio import sleep as async_sleep
from bs4 import BeautifulSoup

# initialize the searchplease translations
namespace.translator.initialize('searchplease')

# the commandline to open new tab in the browser
browsers = {
    'Chrome': 'start chrome.exe ',
    'Opera': 'start "C:\\Program Files (x86)\\Opera\\launcher.exe" --ran-launcher --remote ',
    'OperaGX': f'start "C:\\Users\\{os.getlogin()}\\AppData\\Local\\Programs\\Opera GX\\launcher.exe" --ran-launcher --remote ',
    'Edge': 'start microsoft-edge:',
    'FireFox': 'start firefox.exe -new-tab',
    'Default': 'start '
}
# search engines links
search_engines = {
    'google': 'https://www.google.com/search?q=',
    'duckduckgo': 'https://www.duckduckgo.com/?q=',
    'yandex': 'https://yandex.com/search/?text='
}

# settings
find_browser     = 'OperaGX'     # change it to your browser
search_engine    = 'duckduckgo'  # change it to your prefer search engine
gsearch_country  = 'ua'          # "gsearch" will search in that country (write country code only!)

search_line = f'{browsers[find_browser]}{search_engines[search_engine]}'

# advanced settings

# headers for the google_search_image_by_query
gsibq_headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0', }


async def unsupported_platform(event, _):
    await namespace.instance.send_unsuccess(event,
                                            namespace.translations['searchplease']['unsupported_platform'])


def google_search_image_by_query(query: str, count: int = 1, output_dir: str = namespace.instance.cache_dir):
    r = request.Request(
        url=f'https://www.google.com/search?hl=jp&q={quote(query)}&btnG=Google+Search&tbs=0&safe=off&tbm=isch',
        headers=gsibq_headers
    )

    # get page and html content
    page = request.urlopen(r)
    html = page.read().decode('utf-8')

    # initalize BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # get elements
    elements = soup.find_all('img')
    elements_dict = dict()

    images_downloaded = []
    counter = 0

    for e in elements:
        if not any(re.findall(r'https?://\S+gstatic.com\S+', e['src'])):
            continue

        # get image url
        img_url = e['src']

        # path to image
        img_path = os.path.join(output_dir, f'img_{counter}.jpg')

        images_downloaded.append(img_path)

        # download image by url
        this.logger.debug(f'Downloading image {img_url} -> {img_path}')
        try:
            request.urlretrieve(img_url, img_path)
            counter += 1

        except Exception as e:
            this.logger.log_exception(e)
            this.logger.debug(f'Can\'t download image {img_url}')

        # check for the downloaded count
        if counter == count:
            break

    return counter, images_downloaded


# opens the browser tab with the query
@this.command(namespace.translations['searchplease']['command']['search']['names'], static_pname='search')
@this.only('windows', alt=unsupported_platform)
async def search(event, args):
    if not len(args) > 1:
        return

    # Execute the commandline to open the query in the browser
    os.system(search_line + quote(' '.join(args)))
    await namespace.instance.send_success(event,
                                          namespace.translations['searchplease']['command']['search']['query_opened'])

namespace.pcommands[search.__name__].append('danger')  # mark this command as danger


# sends the results of search from the Google to the telegram chat
@this.command(namespace.translations['searchplease']['command']['gsearch']['names'])
async def gsearch_(event, args):

    # if first number is numeric - type-cast it into int and use it as number of result
    num = 1
    if args[1].isnumeric():
        num = int(args[1])

    if event.reply_to:
        # find the "reply to" message
        msg = [msg async for msg in namespace.instance.client.iter_messages(event.chat_id, 25)
                        if msg.id == event.reply_to.reply_to_msg_id]
        text = msg[0].message
    else:
        if not len(args) > 1:
            return

        text = ' '.join(args[2:]) if num > 1 else ' '.join(args[1:])

    # Send query to the Google
    for url in gsearch(text, stop=num, num=num):
        await namespace.instance.send_success(
            event,
            namespace.translations['searchplease']['command']['gsearch']['link_found'].format(url)
        )
        await async_sleep(0.2)

    namespace.temp_files.append(os.path.join(namespace.instance.install_dir, '.google-cookie'))


@this.command(namespace.translations['searchplease']['command']['gimgsearch']['names'])
async def gimgsearch(event, args):

    # if first number is numeric - type-cast it into int and use it as number of result
    count = 1
    if args[1].isnumeric():
        count = int(args[1])

    if event.reply_to:
        # find the "reply to" message
        msg = [msg async for msg in namespace.instance.client.iter_messages(event.chat_id, 25)
                        if msg.id == event.reply_to.reply_to_msg_id]
        text = msg[0].message
    else:
        if not len(args) > 1:
            return

        text = ' '.join(args[2:]) if count > 1 else ' '.join(args[1:])

    # send message about success results
    await namespace.instance.send_success(
        event,
        namespace.translations['searchplease']['command']['gimgsearch']['results_message']
    )

    # send founded images
    for path in google_search_image_by_query(text, count)[1]:
        await namespace.instance.client.send_file(event.chat_id, path)
        await async_sleep(0.2)


namespace.searchplease = namespace.Namespace()
namespace.searchplease.google_search_image_by_query = google_search_image_by_query
namespace.searchplease.gsearch = gsearch

# TODO: Search by image
