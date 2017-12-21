# -*- coding: utf-8 -*-
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import MessageHandler, CommandHandler, CallbackQueryHandler, Filters

from core.handlers.decorators import save_chanel_decorator
from core.handlers.finder import parse_result, normalize_download_url
from core.handlers.messages import Messages
from core.paging.page import Page
import json

messages = Messages()


def build_download_keyboard(songs_data):
    download_buttons = []
    for data in songs_data:

        title = data[0]
        url = data[1]

        data = json.dumps({'provider': 'zaycev_net', 'link': url})
        print('DATA: ', data)
        print('TYPE: ', type(data))
        print('SIZE: ', len(url))
        print('SIZE: ', len(data.encode('utf-8')))

        inline_download_button = InlineKeyboardButton(title, callback_data=data)
        download_buttons.append([inline_download_button])
    print(download_buttons)
    return download_buttons


def attach_pager_buttons(buttons, pager, song_name):
    limit, offset = pager.limit, pager.offset
    pagination_buttons = [[]]

    prev_callback_template = 'pager.prev.limit.{}.offset.{}.track_name.{}'
    next_callback_template = 'pager.next.limit.{}.offset.{}.track_name.{}'

    prev_callback = prev_callback_template.format(limit, offset, song_name)
    next_callback = next_callback_template.format(limit, offset, song_name)

    if pager.has_prev:
        pagination_buttons[0].append(InlineKeyboardButton('<<<', callback_data=prev_callback))

    if pager.has_next:
        pagination_buttons[0].append(InlineKeyboardButton('>>>', callback_data=next_callback))

    return pagination_buttons + buttons + pagination_buttons


@save_chanel_decorator
def search_audio(bot, update):
    messages.set_language(bot.area.language)
    bot.send_message(update.message.chat.id, messages.get_massage('searching'))
    limit, offset = 5, 0
    keyboard = make_markup_keyboard(bot, update.message.chat.id, update.message.text, limit, offset)

    try:
        if keyboard:
            bot.send_message(update.message.chat.id, messages.get_massage('i_find'), reply_markup=keyboard)
        else:
            bot.send_message(update.message.chat.id, messages.get_massage('i_try'))
    except Exception as ex:
        print(ex)

def make_markup_keyboard(bot, chat_id, text, limit, offset):
    try:
        songs_data, songs_count = parse_result(text, limit, offset)
        songs_data = list(filter(None, songs_data))

        pager = Page(songs_count, limit, offset)

        songs_buttons = build_download_keyboard(songs_data)

        if songs_buttons:
            buttons = attach_pager_buttons(songs_buttons, pager, text)
            keyboard = InlineKeyboardMarkup(buttons)
            return keyboard

    except Exception as ex:
        print(ex)
    return None


def next_page(bot, update, *args, **kwargs):
    query = update.callback_query

    limit = int(query.data.split('.')[3])
    offset = int(query.data.split('.')[5])
    song_name = query.data.split('.')[7]

    edit_markup(bot, update.callback_query.message.chat_id, update.callback_query.message.message_id, song_name, limit,
                offset + limit)


def prev_page(bot, update, *args, **kwargs):
    query = update.callback_query

    limit = int(query.data.split('.')[3])
    offset = int(query.data.split('.')[5])
    song_name = query.data.split('.')[7]

    edit_markup(bot, update.callback_query.message.chat_id, update.callback_query.message.message_id, song_name, limit,
                offset - limit)


def edit_markup(bot, chat_id, message_id, song_name, limit, offset):
    keyboard = make_markup_keyboard(bot, chat_id, song_name, limit, offset)
    bot.edit_message_reply_markup(chat_id=chat_id,
                                  message_id=message_id,
                                  inline_message_id=None,
                                  reply_markup=keyboard)


@save_chanel_decorator
def send_info(bot, update):
    messages.set_language(bot.area.language)
    message = messages.get_massage('intro')
    return bot.send_message(update.message.chat.id, message)


def get_track_link(query_data):
    try:
        result = json.loads(query_data)['link']
    except Exception as e:
        print(e)
        result = query_data

    return result

def get_provider_type(query_data):
    try:
        result = json.loads(query_data)['provider']
    except Exception as e:
        print(e)
        result = 'zaycev_net'

    return result

@save_chanel_decorator
# @save_download_decorator
def download_song(bot, update, *args, **kwargs):
    messages.set_language(bot.area.language)
    query = update.callback_query

    print('QUERY: ', query)

    track_link = get_track_link(query.data)
    provider = get_provider_type(query.data)

    download_url = normalize_download_url(track_link, provider)
    bot.send_audio(query.message.chat_id, download_url)


def init_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler('start', send_info))
    dispatcher.add_handler(MessageHandler(Filters.text, search_audio))
    dispatcher.add_handler(CallbackQueryHandler(prev_page, True, False, 'pager.prev.*'))
    dispatcher.add_handler(CallbackQueryHandler(next_page, True, False, 'pager.next.*'))
    dispatcher.add_handler(CallbackQueryHandler(download_song, pass_update_queue=True))
    return dispatcher


if __name__ == '__main__':
    example_data = '/musicset/play/4ba0a8adb8da96f69b0a8919da9fb0fb/1611152.json'
    example_data = json.dumps({'provider': 'Deezer', 'link': '/musicset/play/4ba0a8adb8da96f69b0a8919da9fb0fb/1611152.json'})

    # x = {'a': 1, 'b': 2}
    # print(type(json.dumps(x)))

    print(get_track_link(example_data))
    print(get_provider_type(example_data))