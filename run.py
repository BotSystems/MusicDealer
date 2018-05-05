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


@app.route('/telegram/search/result', methods=['POST'])
def send_menu_data():
    data = {
        'data': {
            'area_id': 1,
            'chanel_id': 292198768,
            'result': [
                [
                    "\u0421\u043e\u0444\u0438\u044f \u0420\u043e\u0442\u0430\u0440\u0443 - \u041b\u0430\u0432\u0430\u043d\u0434\u0430",
                    "/musicset/play/2fc023f4a3ecbc19edc6fd7e63e53bcf/899010.json",
                    "zaycev_net"
                ],
                [
                    "\u0421\u043e\u0444\u0438\u044f \u0420\u043e\u0442\u0430\u0440\u0443 - \u0425\u0443\u0442\u043e\u0440\u044f\u043d\u043a\u0430 ",
                    "/musicset/play/073fc2d7c71cdec0b80f4196155f5855/1682418.json",
                    "zaycev_net"
                ],
                [
                    "\u0421\u043e\u0444\u0438\u044f \u0420\u043e\u0442\u0430\u0440\u0443 - \u0412\u0430\u043b\u0435\u043d\u0442\u0438\u043d\u0430",
                    "/musicset/play/3aeb74387e30e213201b127bcf07941a/2391566.json",
                    "zaycev_net"
                ]
            ]
        }
    }

    area = Area.select().where(Area.id == data['data']['area_id']).first()
    selected_bot = storage.get(area.token)

    selected_bot.send_message(data['data']['chanel_id'], 'test')


@app.route('/telegram/download/result', methods=['POST'])
def send_download_data():
    pass


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
