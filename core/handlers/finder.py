# -*-coding: utf-8;-*-
import os
from urllib.parse import urljoin, urlencode, urlsplit

import requests

SEARCH_URL = os.getenv('SEARCH_TRACKS_TEMPLATE')
DOWNLOAD_URL = os.getenv('DOWNLOAD_TRACK_TEMPLATE')


def parse_result(normalized_song_name, limit, offset):
    search_page_url = SEARCH_URL.format(normalized_song_name)
    search_page = requests.get(search_page_url, params={'page[limit]': limit, 'page[offset]': offset})

    return [search_page.json()['data'], search_page.json()['meta']['total']]


def normalize_download_url(data_url, provider):
    # url = 'https://track-finder.herokuapp.com/download?{}'
    params = {'url': data_url, 'provider': provider}

    result = requests.get(DOWNLOAD_URL.format(urlencode(params))).json()
    if 'data' in result:
        return result['data']['download_url']
    return None


# def normalize_download_url_old(data_url):
#     url = urljoin('http://zaycev.net', data_url)
#     result = requests.get(url).json()
#     url = dict(result).get('url')
#     if url:
#         url = str.split(url, '?')
#     if url:
#         return url[0]
#     return None


if __name__ == '__main__':
    # data_urls = parse_result('The Hardkiss')
    # print(data_urls)

    download_url = normalize_download_url("/musicset/play/936394cc1b6ac6e01ea123f96033bd8a/3946953.json", 'zaycev_net')
    print(download_url)

    # download_url1 = normalize_download_url1("/musicset/play/936394cc1b6ac6e01ea123f96033bd8a/3946953.json")
    # print(download_url1)