# -*-coding:utf-8;-*-
from abc import ABCMeta, abstractmethod


class AwarePayloadBuildMethod(metaclass=ABCMeta):

    @abstractmethod
    def build_payload(self):
        raise Exception('Implement me!')


class UserRequest(metaclass=ABCMeta):
    token = None
    channel_id = None
    language = None

    def __init__(self, token, channel_id, language):
        self.token = token
        self.channel_id = channel_id
        self.language = language


class SearchTask(UserRequest, AwarePayloadBuildMethod):
    ACTION_TYPE = 'search'

    query = None
    limit = None
    offset = None

    parent_message_id = None
    postback_url = None

    def __init__(self, token, channel_id, language, query, parent_message_id, limit, offset, postback_url):
        super(SearchTask, self).__init__(token, channel_id, language)
        self.query = query
        self.limit = limit
        self.offset = offset
        self.parent_message_id = parent_message_id
        self.postback_url = postback_url

    def build_payload(self):
        return {'channel_id': self.channel_id,
                'action_type': self.ACTION_TYPE,
                'token': self.token,
                'language': self.language,
                'query': self.query,
                'parent_message_id': self.parent_message_id,
                'limit': self.limit,
                'offset': self.offset,
                'postback_url': self.postback_url}


class DownloadTask(UserRequest, AwarePayloadBuildMethod):
    ACTION_TYPE = 'download'

    url = None
    provider = None
    postback_url = None

    def __init__(self, token, channel_id, language, url, provider, postback_url):
        super(DownloadTask, self).__init__(token, channel_id, language)
        self.url = url
        self.provider = provider
        self.postback_url = postback_url

    def build_payload(self):
        return {'channel_id': self.channel_id,
                'action_type': self.ACTION_TYPE,
                'token': self.token,
                'language': self.language,
                'url': self.url,
                'provider': self.provider,
                'postback_url': self.postback_url}


class UploadTask(AwarePayloadBuildMethod):
    download_url = None

    def __init__(self, download_url):
        self.download_url = download_url

    def build_payload(self):
        return {'url': self.download_url}
