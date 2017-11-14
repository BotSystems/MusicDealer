# -*-coding: utf-8;-*-
import os
from urllib.parse import urljoin

import requests

SEARCH_URL = os.getenv('SEARCH_TRACKS_TEMPLATE')
DOWNLOAD_URL = os.getenv('DOWNLOAD_TRACK_TEMPLATE')


def parse_result(normalized_song_name):
    search_page_url = SEARCH_URL.format(normalized_song_name)
    search_page = requests.get(search_page_url)

    return search_page.json()['data']


def normalize_download_url(data_url):
    url = urljoin('http://zaycev.net', data_url)
    result = requests.get(url).json()
    url = dict(result).get('url')
    if url:
        url = str.split(url, '?')
    if url:
        return url[0]
    return None


if __name__ == '__main__':
    data_urls = parse_result('The Hardkiss')
    print(data_urls)

    download_url = normalize_download_url("/musicset/play/936394cc1b6ac6e01ea123f96033bd8a/3946953.json")
    print(download_url)
