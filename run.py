import os

import telegram
from flask import Flask, request

app = Flask(__name__)

from core.bot.factory import Factory
from core.bot.storage import Storage
from core.area.models import Area

storage = Storage(Factory())
storage.create([area for area in Area.select()])


@app.route('/', methods=['GET'])
def index():
    return 'index'


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

    app.run(host='0.0.0.0', port=port, debug=debug)
