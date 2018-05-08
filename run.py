import json
import os
import telegram
from flask import Flask, request
from flask import Response

from core.handlers.handler import make_markup_keyboard
from core.paging.page import Page
from core.task.prepare import task_storage as amqp_task_storage

app = Flask(__name__)

from core.bot.factory import Factory
from core.bot.storage import Storage
from core.area.models import Area

storage = Storage(Factory())
storage.create([area for area in Area.select()])

# use only for create instance
task_storage = amqp_task_storage


@app.route('/', methods=['GET'])
def index():
    # todo: show statistics
    return 'index'


@app.route('/telegram/search/result', methods=['POST'])
def send_menu_data():
    try:
        data = request.get_json()

        content = data['content']
        meta = data['meta']

        token = meta['token']
        selected_bot = storage.get(token)

        pager = Page(content['meta']['total'], content['meta']['limit'], content['meta']['offset'])
        keyboard = make_markup_keyboard(meta['query'], content['data'], pager)
        selected_bot.send_message(meta['chat_id'], 'test', reply_markup=keyboard)

        return Response(json.dumps({'status': 'ok'}), 200)
    except Exception as ex:
        return Response(json.dumps({'status': 'error'}), 500)


@app.route('/telegram/download/result', methods=['POST'])
def send_download_data():
    try:
        data = request.get_json()

        content = data['content']
        meta = data['meta']

        token = meta['token']

        selected_bot = storage.get(token)

        selected_bot.send_audio(meta['chat_id'], content['data']['download_url'])

        return Response(json.dumps({'status': 'ok'}), 200)
    except Exception as ex:
        return Response(json.dumps({'status': 'error'}), 500)


@app.route('/<token>', methods=['POST'])
def webhook_handler(token):
    selected_bot = storage.get(token)
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), selected_bot)
        selected_bot.dispatcher.process_update(update)
    return 'ok!'


if __name__ == '__main__':
    port = int(os.getenv('PORT'))
    debug = os.getenv('DEBUG')

    app.run(host='0.0.0.0', port=5024, debug=debug)
