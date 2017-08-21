# -*-coding: utf-8;-*-
import requests

from handlers.audio_parsers import prepare_result

SEARCH_URL = 'http://zaycev.net/search.html?query_search={song_name}'
DOWNLOAD_URL = 'http://zaycev.net'

# html_parser = ZaycevNetAudioParser()


def normalize_song_name(song_name):
    return str.replace(song_name, ' ', '+')


def parse_result(normalized_song_name):
    search_page_url = SEARCH_URL.format(song_name=normalized_song_name)
    search_page = requests.get(search_page_url)

    # Parsing
    # html_parser = prepare_result(search_page.content.decode())
    # html_parser.find_results()


    # html_parser.feed(search_page.content.decode())
    # result, parser = html_parser.get_result()
    # parser.clear_all()
    return prepare_result(search_page.content.decode())


def normalize_download_url(data_url):
    # todo: use url splitter
    url = DOWNLOAD_URL + data_url
    result = requests.get(url).json()
    url = dict(result).get('url')
    if url:
        url = str.split(url, '?')
    if url:
        return url[0]
    return None


if __name__ == '__main__':
    data_urls = parse_result(normalize_song_name('The Hardkiss'))
    print(data_urls)
    # download_urls = [get_download_urls(url) for url in data_urls ]
    # download_urls.append(None)
    # download_urls = list(filter(None, download_urls))
    # print(download_urls)
