# -*-coding: utf-8;-*-
import os
from urllib.parse import urljoin

import requests

from core.handlers.audio_parsers import prepare_result

SEARCH_URL = os.getenv('SEARCH_TRACKS_TEMPLATE')
DOWNLOAD_URL = os.getenv('DOWNLOAD_TRACK_TEMPLATE')


def normalize_song_name(song_name):
    return song_name
    # return str.replace(song_name, ' ', '+')


def parse_result(normalized_song_name):
    search_page_url = SEARCH_URL.format(normalized_song_name)
    search_page = requests.get(search_page_url)

    return prepare_result(search_page.json()['data'])


def normalize_download_url(data_url):
    url = DOWNLOAD_URL.format(data_url)
    result = requests.get(url).json()
    if 'data' in result:
        return result['data']['download_url']
    return None


if __name__ == '__main__':
    data_urls = parse_result(normalize_song_name('The Hardkiss'))
    print(data_urls)

    download_url = normalize_download_url("/musicset/play/936394cc1b6ac6e01ea123f96033bd8a/3946953.json")
    print(download_url)
