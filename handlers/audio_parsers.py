from html.parser import HTMLParser


class ZaycevNetAudioParser(HTMLParser):
    status = False
    result = []
    data_urls = []

    def parse_data_url(self, attrs):
        for k, v in attrs:
            if k != 'data-url':
                continue
            return v

        return None

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for k, v in attrs:
                if k != 'class':
                    continue
                if v != 'musicset-track clearfix':
                    continue

                data_url = self.parse_data_url(attrs)
                if data_url is not None:
                    self.data_urls.append(data_url)

    def handle_data(self, data):
        if self.status:
            self.save_to_result(data)

    def save_to_result(self, data):
        self.result.append(data)

    def clear_all(self):
        self.reset()
        self.status = False
        self.data_urls = []

    def get_result(self):
        if self.data_urls:
            return (self.data_urls[0], self)
        return (None, self)
