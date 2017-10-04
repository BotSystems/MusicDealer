import os

import telegram
from flask import Flask, request
from telegram.ext import Dispatcher

from bot_manager import Bot
from handlers.handler import init_handlers

app = Flask(__name__)
from models import Area

bots = dict()
# Create bots
areas = Area.select()

for _area in areas:
    _bot = Bot(_area.token)
    _dispatcher = init_handlers(Dispatcher(_bot, None, workers=0))
    _bot.add_dispatcher(_dispatcher)
    _bot.add_area(_area)

    bots[_bot.area.token] = _bot


# bot = telegram.Bot(os.getenv('TOKEN'))
# dispatcher = init_handlers(Dispatcher(bot, None, workers=0))


@app.route('/<token>', methods=['GET', 'POST'])
def webhook_handler(token):
    print(token)
    selected_bot = bots[token]
    print(selected_bot)
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), selected_bot)
        selected_bot.dispatcher.process_update(update)
    return 'ok!'


if __name__ == '__main__':
    port = int(os.getenv('PORT'))
    debug = os.getenv('DEBUG')

    app.run(host='0.0.0.0', port=port, debug=debug)
