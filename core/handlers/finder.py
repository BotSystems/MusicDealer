# -*-coding: utf-8;-*-
import os
from urllib.parse import urljoin

import requests

from core.handlers.audio_parsers import prepare_result

SEARCH_URL = os.getenv('SEARCH_TRACKS_TEMPLATE', 'http://127.0.0.1:5000/search?query={}')
DOWNLOAD_URL = os.getenv('DOWNLOAD_TRACK_TEMPLATE', )


def normalize_song_name(song_name):
    return song_name
    # return str.replace(song_name, ' ', '+')


def parse_result(normalized_song_name):
    search_page_url = SEARCH_URL.format(normalized_song_name)
    search_page = requests.get(search_page_url)

    return prepare_result(search_page.json()['data'])


def normalize_download_url(data_url):
    url = urljoin(DOWNLOAD_URL, data_url)
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
