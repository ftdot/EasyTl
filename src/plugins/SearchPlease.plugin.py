# begin info
#   description = "Library-plugin | Allows to manage the commands permissions"
#   required_platforms = [ "windows", "linux", "android" ]
#   required_plugins = "no requirements"
#   etl_version_min = [ 1, 4, 0 ]
#   etl_version_max = [ 1, 4, "*" ]
#   version = "1.5.1"
#   update_link = "https://github.com/ftdot/EasyTl/raw/master/easytl-cli/plugins/SearchPlease.plugin.py"
#   lang_links = [ ["searchplease_en.toml", "https://github.com/ftdot/EasyTl/raw/master/easytl-cli/translations/searchplease_en.toml"], ["searchplease_ru.toml", "https://github.com/ftdot/EasyTl/raw/master/easytl-cli/translations/searchplease_ru.toml"], ["searchplease_uk.toml", "https://github.com/ftdot/EasyTl/raw/master/easytl-cli/translations/searchplease_uk.toml"] ]
#   requirements = [ "google", "BeautifulSoup4" ]
#   author = "ftdot (https://github.com/ftdot)"
#   changelog = [ "Changed default settings" ]
# end info


import os
import re
from urllib import request
from urllib.parse import quote
from googlesearch import search as gsearch
from asyncio import sleep as async_sleep
from bs4 import BeautifulSoup
from source.argumentparser import ArgumentParser, Argument, Cast

# initialize the searchplease translations
namespace.translator.initialize('searchplease')

# the commandline to open new tab in the browser
browsers = {
    'Chrome': 'chrome.exe ',
    'Opera': '"C:\\Program Files (x86)\\Opera\\launcher.exe" --ran-launcher --remote ',
    'OperaGX': f'"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Programs\\Opera GX\\launcher.exe" --ran-launcher --remote ',
    'Edge': 'microsoft-edge:',
    'FireFox': 'firefox.exe -new-tab',
    'Default': 'start '
}
# search engines links
search_engines = {
    'google': 'https://www.google.com/search?q=',
    'duckduckgo': 'https://www.duckduckgo.com/?q=',
    'yandex': 'https://yandex.com/search/?text='
}

# settings
find_browser     = 'Default'     # change it to your browser
search_engine    = 'google'      # change it to your prefer search engine
gsearch_country  = 'us'          # "gsearch" will search in that country (write only ISO 3166-alpha-2 code)

search_line = f'{browsers[find_browser]}{search_engines[search_engine]}'

# advanced settings

# headers for the google_search_image_by_query
gsibq_headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0', }


####


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

    # initialize BeautifulSoup
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

####


# opens the browser tab with the query
@this.command(namespace.translations['searchplease']['command']['search']['names'],
              ap=ArgumentParser(this, [Argument('search_string'), ]),
              static_pname='search')
@this.only('windows', alt=unsupported_platform)
async def search(event, args):
    # Execute the commandline to open the query in the browser
    os.system(search_line + quote(args.search_string))
    await namespace.instance.send_success(event,
                                          namespace.translations['searchplease']['command']['search']['query_opened'])

if search is not unsupported_platform:
    namespace.pcommands[search.__name__].append('danger')  # mark this command as danger


# sends the results of search from the Google to the telegram chat
@this.command(namespace.translations['searchplease']['command']['gsearch']['names'],
              ap=ArgumentParser(this, [Argument('search_string', default='<<reply_to>>'),
                                       Argument('number', Cast.IntCast, 1)])
              )
async def gsearch_(event, args):

    if args.search_string == '<<reply_to>>':
        if not event.reply_to:
            return

        # find the "reply to" message
        msg = [msg async for msg in namespace.instance.client.iter_messages(event.chat_id, 25)
                        if msg.id == event.reply_to.reply_to_msg_id]
        text = msg[0].message
    else:
        text = args.search_string

    # Send query to the Google
    for url in gsearch(text, stop=args.number, num=args.number):
        await namespace.instance.send_success(
            event,
            namespace.translations['searchplease']['command']['gsearch']['link_found'].format(url)
        )
        await async_sleep(0.2)

    namespace.temp_files.append(os.path.join(namespace.instance.install_dir, '.google-cookie'))


@this.command(namespace.translations['searchplease']['command']['gimgsearch']['names'],
              ap=ArgumentParser(this, [Argument('search_string', default='<<reply_to>>'),
                                       Argument('number', Cast.IntCast, 1)])
              )
async def gimgsearch(event, args):

    if args.search_string == '<<reply_to>>':
        if not event.reply_to:
            return

        # find the "reply to" message
        msg = [msg async for msg in namespace.instance.client.iter_messages(event.chat_id, 25)
                        if msg.id == event.reply_to.reply_to_msg_id]
        text = msg[0].message
    else:
        text = args.search_string

    # send message about success results
    await namespace.instance.send_success(
        event,
        namespace.translations['searchplease']['command']['gimgsearch']['results_message']
    )

    # send founded images
    for path in google_search_image_by_query(text, args.number)[1]:
        await namespace.instance.client.send_file(event.chat_id, path)
        await async_sleep(0.2)


namespace.searchplease = namespace.Namespace()
namespace.searchplease.google_search_image_by_query = google_search_image_by_query
namespace.searchplease.gsearch = gsearch

# TODO: Search by image
