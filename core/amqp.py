import json
import os
import random
import pika

CLOUDAMQP_URL = os.getenv('CLOUDAMQP_URL')
QUEUE = os.getenv('QUEUE_NAME')

def upload_to_queue(download_url):
    pass
    # if (2 == random.randint(1, 2)):
    #     parameters = pika.URLParameters(CLOUDAMQP_URL)
    #     connection = pika.BlockingConnection(parameters)
    #
    #     channel = connection.channel()
    #     data = {'payload': {'url': download_url}}
    #
    #     try:
    #         channel.basic_publish('', QUEUE, json.dumps(data), pika.BasicProperties(content_type='text/plain', delivery_mode=1))
    #     except Exception as ex:
    #         print(ex.message)
    #     finally:
    #         connection.close()

if __name__ == '__main__':
    upload_to_queue('https://example.com')
    print('ok')
