import json
import os
import random

import pika

CLOUDAMQP_URL = os.getenv('CLOUDAMQP_URL')
# PORT = os.getenv('PORT')
# USER = os.getenv('USER')
# PASSWORD = os.getenv('PASSWORD')
# VHOST = os.getenv('VHOST')

# credentials = pika.PlainCredentials(USER, PASSWORD)
parameters = pika.URLParameters(CLOUDAMQP_URL)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()
channel.exchange_declare(exchange="downloads", exchange_type="direct",
                         passive=False, durable=True, auto_delete=False)


def upload_to_queue(download_url):
    data = {'payload': {'url': download_url}}

    try:
        print("Sending message to create a queue")
        channel.basic_publish('downloads', '', json.dumps(data),
                              pika.BasicProperties(content_type='text/plain', delivery_mode=1))
        print(" [x] upload to queue: ".format(download_url))
        connection.close()
    except Exception as ex:
        print(ex.message)

if __name__ == '__main__':
    upload_to_queue('https://example.com')
    print('ok')
