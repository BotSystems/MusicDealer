# -*-coding: utf-8;-*-
import requests

from handlers.audio_parsers import ZaycevNetAudioParser

SEARCH_URL = 'http://zaycev.net/search.html?query_search={song_name}'
DOWNLOAD_URL = 'http://zaycev.net'

html_parser = ZaycevNetAudioParser()


def normalize_song_name(song_name):
    return str.replace(song_name, ' ', '+')


def search_first_data_url(normalized_song_name):
    search_page_url = SEARCH_URL.format(song_name=normalized_song_name)
    search_page = requests.get(search_page_url)
    html_parser.feed(search_page.content.decode())
    result, parser = html_parser.get_result()
    parser.clear_all()
    return result


def get_download_url(data_url):
    if data_url is None:
        return None

    url = DOWNLOAD_URL + data_url
    result = requests.get(url).json()
    url = dict(result).get('url')
    if url:
        url = str.split(url, '?')
    if url:
        return url[0]
    return None


if __name__ == '__main__':
    data_url = search_first_data_url(normalize_song_name('The Hardkiss - Make-Up'))
    print(get_download_url(data_url))
