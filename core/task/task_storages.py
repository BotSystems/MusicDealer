import json
import pika

from core.task.task_types import UploadTask


class AmqpStorage:
    QUEUES = {
        'SearchTask':   'user_request',
        'DownloadTask': 'user_request',
        'UploadTask':   'track_downloads',
    }

    connection = None
    channel = None
    parameters = None

    def __init__(self, cloud_amqp_url):
        self.parameters = pika.URLParameters(cloud_amqp_url)


    def publish(self, task):
        queue = self.QUEUES.get(task.__class__.__name__)

        data = json.dumps({'payload': task.build_payload()})
        properties = pika.BasicProperties(content_type='text/plain', delivery_mode=1)

        # channel = self.connection.channel()
        try:
            self.connection = pika.BlockingConnection(self.parameters)
            self.channel = self.connection.channel()
            self.channel.exchange_declare('user_actions')
            self.channel.basic_publish('user_actions', 'actions', data, properties)
            print('Add task has been successfully')
        except Exception as ex:
            print('Exception: ', str(ex))

        try:
            self.connection.close()
        except Exception:
            pass


if __name__ == '__main__':
    token = ''
    chat_id = ''
    language = ''
    query = 'hardkiss'
    limit = 5
    offset = 0
    url = ''
    provider = 'zaycev_net'

    print('-' * 10)
    storage = AmqpStorage('amqp://pbiolrgp:QhFRfvRmEczAM_ASOSWyBOJW0lbK-nGN@hornet.rmq.cloudamqp.com/pbiolrgp')

    # search task
    # task1 = SearchTask('same-secret-token')
    # storage.publish(task1)

    # download task
    # task2 = DownloadTask()
    # storage.publish(task2)

    # upload task
    task3 = UploadTask('ooops')
    storage.publish(task3)
    print('-' * 10)
