# -*-coding:utf-8;-*-
from abc import ABCMeta, abstractmethod


class AwarePayloadBuildMethod(metaclass=ABCMeta):

    @abstractmethod
    def build_payload(self):
        raise Exception('Implement me!')


class UserRequest(metaclass=ABCMeta):
    token = None
    language = None

    def __init__(self, token, language):
        self.token = token
        self.language = language


class SearchTask(UserRequest, AwarePayloadBuildMethod):
    ACTION_TYPE = 'search'

    query = None
    limit = None
    offset = None

    def __init__(self, token, language, query, limit, offset):
        super(SearchTask, self).__init__(token, language, query, limit, offset)
        self.query = query
        self.limit = limit
        self.offset = offset

    def build_payload(self):
        return {'action_type': self.ACTION_TYPE, 'token': self.token, 'language': self.language, 'query': self.query,
                'limit':       self.limit,
                'offset':      self.offset}


class DownloadTask(UserRequest, AwarePayloadBuildMethod):
    ACTION_TYPE = 'download'

    url = None
    provider = None

    def __init__(self, token, language, url, provider):
        super(DownloadTask, self).__init__(token, language, url, provider)
        self.url = url
        self.provider = provider

    def build_payload(self):
        return {'action_type': self.ACTION_TYPE, 'token': self.token, 'language': self.language, 'url': self.url,
                'provider':    self.provider}


class UploadTask(AwarePayloadBuildMethod):
    download_url = None

    def __init__(self, download_url):
        self.download_url = download_url

    def build_payload(self):
        return {'url': self.download_url}
