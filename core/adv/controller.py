import json
import os

from core.adv.factory import Factory
from core.adv.storage import Storage
from core.download.models import Download

adv_source = os.path.join(os.path.dirname(__file__), 'advertising.json')
with open(adv_source, encoding='utf-8') as advs_data:
    advs = json.load(advs_data)

storage = Storage(Factory())
storage.create(advs.get('data', []))


def send_adv(bot, chat_id, messages):
    try:
        if (len(Download.select()) % int(os.getenv('SEND_ADV_PER_ACTION', 5)) == 0):
            adv = storage.get()
            bot.send_message(chat_id, adv.build_message(), reply_markup=adv.build_keyboard(messages), parse_mode='Markdown')
    except Exception as ex:
        print('Exception: ', ex)
