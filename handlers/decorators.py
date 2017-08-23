# -*- coding: utf-8 -*-
import os

from botanio import botan

from models import Chanel

BOTAN_TOKEN = os.getenv('BOTAN_TOKEN')


def save_chanel_decorator(fn):
    def wrapper(bot, update, *args, **kwargs):
        print('SAVE CHANEL')

        try:
            if(update.callback_query):
                first_name = update.callback_query.message.chat.first_name
                last_name = update.callback_query.message.chat.last_name
            else:
                first_name = update.message.chat.first_name
                last_name = update.message.chat.last_name

            defaults = {'chanel_id': update.message.chat.id, 'first_name': first_name, 'last_name': last_name}
            chanel, is_new = Chanel.get_or_create(chanel_id=update.message.chat.id, defaults=defaults)
            chanel.save()
        except Exception as ex:
            print(ex)

        return fn(bot, update, *args, **kwargs)

    return wrapper


def botan_decorator(event_name):
    def real_decorator(fn):
        def wrapper(bot, update, *args, **kwargs):
            chat_id = update.message.chat_id
            message = update.message.text
            botan.track(BOTAN_TOKEN, chat_id, message, event_name)
            return fn(bot, update)

        return wrapper

    return real_decorator
