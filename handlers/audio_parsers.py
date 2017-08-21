from html.parser import HTMLParser
from bs4 import BeautifulSoup

# bs4 = BeautifulSoup()


# class ZaycevNetAudioParser(HTMLParser):
#     status = False
#     result = []
#     data_urls = []
#
#     def parse_data_url(self, attrs):
#         for k, v in attrs:
#             if k != 'data-url':
#                 continue
#             return v
#
#         return None
#
#     def handle_starttag(self, tag, attrs):
#         if tag == 'div':
#             for k, v in attrs:
#                 if k != 'class':
#                     continue
#                 if v != 'musicset-track clearfix':
#                     continue
#
#                 print(attrs)
#
#                 data_url = self.parse_data_url(attrs)
#                 if data_url is not None:
#                     self.data_urls.append(data_url)
#
#     def handle_data(self, data):
#         if self.status:
#             print(data)
#             self.save_to_result(data)
#
#     def save_to_result(self, data):
#         self.result.append(data)
#
#     def clear_all(self):
#         self.reset()
#         self.status = False
#         self.data_urls = []
#
#     def get_result(self):
#         if self.data_urls:
#             return (self.data_urls, self)
#         return (None, self)

def prepare_result(html):
    result = []

    result_div_html = find_result_div(html)
    result_items_html = find_result_items(result_div_html)

    for result_item in result_items_html:
        artist = find_artist_name(result_item)
        song = find_song_title(result_item)
        data_url = find_data_url(result_item)
        result.append(('{} - {}'.format(artist, song), data_url))

    return result

def find_result_div(html):
    parser = BeautifulSoup(html, "html.parser")
    return parser.find('div', {'class': 'musicset-track-list__items'})

def find_result_items(bs_tag):
    return bs_tag.findAll('div', {'class': 'musicset-track clearfix'})

def find_artist_name(bs_tag):
    return bs_tag.find('div', {'class': 'musicset-track__artist'}).find('a', {'class': 'musicset-track__link'}).text

def find_song_title(bs_tag):
    return bs_tag.find('div', {'class': 'musicset-track__track-name'}).find('a', {'class': 'musicset-track__link'}).text

def find_data_url(bs_tag):
    return bs_tag.get('data-url')


if __name__ == '__main__':
    import requests

    url = 'http://zaycev.net/search.html?query_search=kasabian'
    html = requests.get(url).content.decode()
    result_div_html = find_result_div(html)
    result_items_html = find_result_items(result_div_html)

    # print(result_items_html)

    for result_item in result_items_html:
        artist = find_artist_name(result_item)
        song = find_song_title(result_item)
        data_url = find_data_url(result_item)
        # print(result_item)

        # print(result_item.find('div', {'class': 'musicset-track__artist'}).find('a', {'class': 'musicset-track__link'}).text)

        print('{} - {} :: {}'.format(artist, song, data_url))
    # for x in result_div_html:
    #     print(x.find('div', {'class': 'musicset-track__artist'}))