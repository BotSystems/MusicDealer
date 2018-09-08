# -*- coding: utf-8 -*-
import os

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import MessageHandler, CommandHandler, CallbackQueryHandler, Filters

from core.chanel.models import Chanel
from core.handlers.decorators import save_chanel_decorator, save_download_decorator
from core.handlers.finder import parse_result, normalize_download_url
from core.handlers.messages import Messages
from core.paging.page import Page
from core.task.prepare import task_storage
from core.task.task_types import UploadTask, SearchTask, DownloadTask

messages = Messages()

PROVIDER_ALIASES = {
    'zaycev_net': 'zn',
    'mail_ru': 'mr'
}

PROVIDER_ALIASES_BACK = {
    'zn': 'zaycev_net',
    'mr': 'mail_ru'
}

ALIASES_DELIMITER = '::'


def build_download_keyboard(songs_data):
    download_buttons = []
    for data in songs_data:
        title = data[0]
        url = data[1]
        provider = data[2]

        provider_alias = PROVIDER_ALIASES[provider]

        data = '{}{}{}'.format(provider_alias, ALIASES_DELIMITER, url)

        inline_download_button = InlineKeyboardButton(title, callback_data=data)
        download_buttons.append([inline_download_button])
    return download_buttons


def attach_donate_buttons(buttons):
    dotate_button = [[InlineKeyboardButton('💵 DONATE', callback_data='call-donate')]]
    return buttons + dotate_button


def attach_pager_buttons(buttons, pager, song_name):
    limit, offset = pager.limit, pager.offset
    pagination_buttons = [[]]

    prev_callback_template = 'pager.prev.limit.{}.offset.{}.track_name.{}'
    next_callback_template = 'pager.next.limit.{}.offset.{}.track_name.{}'

    prev_callback = prev_callback_template.format(limit, offset, song_name)
    next_callback = next_callback_template.format(limit, offset, song_name)

    if pager.has_prev:
        pagination_buttons[0].append(InlineKeyboardButton('◀️', callback_data=prev_callback))

    if pager.has_next:
        pagination_buttons[0].append(InlineKeyboardButton('▶️', callback_data=next_callback))

    return pagination_buttons + buttons + pagination_buttons


def is_from_group(update):
    return update.channel_post


@save_chanel_decorator
def search_track(bot, update):
    try:
        task = SearchTask(bot.area.token, update.message.chat.id, bot.area.language, update.message.text, None, Page.DEFAULT_LIMIT, Page.DEFAULT_OFFSET, os.getenv('POSTBACK_SEARCH_URL'))
        task_storage.publish(task)
    except Exception as ex:
        print(ex)

    # messages.set_language(bot.area.language)
    # message = bot.send_message(update.message.chat.id, messages.get_massage('searching'))
    #
    # keyboard = get_keyboard(update.message.text, Page.DEFAULT_LIMIT, Page.DEFAULT_OFFSET)
    #
    # try:
    #     if keyboard:
    #         bot.edit_message_text(messages.get_massage('i_find'), update.message.chat.id, message.message_id, reply_markup=keyboard)
    #     else:
    #         bot.send_message(update.message.chat.id, messages.get_massage('i_try'))
    # except Exception as ex:
    #     print('Exception: ', ex.message)


def broadcast(bot, update):
    print('BROADCAST')
    channels = Chanel.select().where(Chanel.area == bot.area)
    chat_ids = [channel.chanel_id for channel in channels]
    print('CHANNELS COUNT: ', len(chat_ids))
    broadcast_success = 0
    broadcast_fail = 0
    for chat_id in chat_ids:
        print('go')
        try:
            bot.forward_message(chat_id, update.channel_post.chat.id, update.channel_post.message_id, True)
            broadcast_success += 1
        except Exception as ex:
            broadcast_fail += 1
            print('Exception: ', ex)
    print('-' * 20)
    print('BROADCAST SUCCESS: {}'.format(broadcast_success))
    print('BROADCAST FAIL: {}'.format(broadcast_fail))
    print('-' * 20)


def is_group_available_for_broadcast(bot, update, callback):
    available_groups = os.getenv('AVAILABLE_CHANNELS', '').split(',')
    if update.channel_post.chat.username in available_groups:
        callback(bot, update)


def handle_message(bot, update):
    if is_from_group(update):
        is_group_available_for_broadcast(bot, update, broadcast)
    else:
        search_track(bot, update)


def get_keyboard(query, limit, offset):
    songs_data, songs_count = search_by_search_query(query, limit, offset)
    pager = Page(songs_count, limit, offset)

    return make_markup_keyboard(query, songs_data, pager)


def search_by_search_query(text, limit, offset):
    songs_data, songs_count = parse_result(text, limit, offset)

    # return song_data, song_count
    return [list(filter(None, songs_data)), songs_count]


def make_markup_keyboard(text, songs_data, pager):
    try:
        songs_buttons = build_download_keyboard(songs_data)

        if songs_buttons:
            buttons = attach_pager_buttons(songs_buttons, pager, text)
            buttons = attach_donate_buttons(buttons)
            keyboard = InlineKeyboardMarkup(buttons)
            return keyboard

    except Exception as ex:
        print('Exception: ', ex.message)
    return None


def next_page(bot, update, *args, **kwargs):
    query = update.callback_query

    limit = int(query.data.split('.')[3])
    offset = int(query.data.split('.')[5])
    song_name = query.data.split('.')[7]

    try:
        task = SearchTask(bot.area.token, update.callback_query.message.chat_id, bot.area.language, song_name, update.callback_query.message.message_id, limit, offset + limit, os.getenv('POSTBACK_SEARCH_URL'))
        task_storage.publish(task)
    except Exception as ex:
        print(ex)

    # edit_markup(bot, update.callback_query.message.chat_id, update.callback_query.message.message_id, song_name, limit,
    #             offset + limit)


def prev_page(bot, update, *args, **kwargs):
    query = update.callback_query

    limit = int(query.data.split('.')[3])
    offset = int(query.data.split('.')[5])
    song_name = query.data.split('.')[7]

    try:
        task = SearchTask(bot.area.token, update.callback_query.message.chat_id, bot.area.language, song_name, update.callback_query.message.message_id, limit, offset - limit, os.getenv('POSTBACK_SEARCH_URL'))
        task_storage.publish(task)
    except Exception as ex:
        print(ex)

    # edit_markup(bot, update.callback_query.message.chat_id, update.callback_query.message.message_id, song_name, limit,
    #             offset - limit)


def edit_markup(bot, chat_id, message_id, song_name, limit, offset):

    # query = song_name
    #
    # songs_data, songs_count = search_by_search_query(query, limit, offset)
    # pager = Page(songs_count, limit, offset)

    keyboard = get_keyboard(song_name, limit, offset)
    try:
        bot.edit_message_reply_markup(chat_id=chat_id,
                                      message_id=message_id,
                                      inline_message_id=None,
                                      reply_markup=keyboard)
    except Exception as ex:
        print('Exception: ', ex.message)


@save_chanel_decorator
def send_info(bot, update):
    messages.set_language(bot.area.language)
    message = messages.get_massage('intro')
    return bot.send_message(update.message.chat.id, message)


def get_track_link(query_data):
    if ALIASES_DELIMITER in query_data:
        return query_data.split(ALIASES_DELIMITER)[1]
    return query_data

    # try:
    #     result = json.loads(query_data)['link']
    # except Exception as e:
    #     print(e)
    #     result = query_data
    #

    # return result


def get_provider_type(query_data):
    if ALIASES_DELIMITER in query_data:
        provider = query_data.split(ALIASES_DELIMITER)[0]
        return PROVIDER_ALIASES_BACK[provider]
    return 'zaycev_net'

    # try:
    #     result = json.loads(query_data)['provider']
    # except Exception as e:
    #     print(e)
    #     result = 'zaycev_net'
    #
    # return result


@save_chanel_decorator
@save_download_decorator
def download_song(bot, update, *args, **kwargs):
    bot.answer_callback_query(update.callback_query.id, messages.get_massage('download'))

    messages.set_language(bot.area.language)
    query = update.callback_query

    track_link = get_track_link(query.data)
    provider = get_provider_type(query.data)

    download_url = normalize_download_url(track_link, provider)
    # print('DOWNLOAD-URL: ', download_url)

    task1 = UploadTask(download_url)
    task_storage.publish(task1)

    task2 = DownloadTask(bot.area.token, query.message.chat_id, bot.area.language, track_link, provider, os.getenv('POSTBACK_DOWNLOAD_URL'))
    task_storage.publish(task2)
    #
    # # upload_to_queue(download_url)
    # bot.send_audio(query.message.chat_id, download_url)


@save_chanel_decorator
def buy(bot, update):
    messages.set_language(bot.area.language)
    message = '''
    Хочешь такого же бота?
Напиши мне @igorkpl
Стоимость подключения - 49$
Средства пойдут на покупку серверов и подключение других музыкальных сервисов.
Добра тебе. '''
    return bot.send_message(update.message.chat.id, message)


@save_chanel_decorator
def donate(bot, update):
    messages.set_language(bot.area.language)
    message = '''
    Как ты уже мог заметить - этот бот абсолютно бесплатный, при этом - он требует вложений, в том числе и финансовых.
Свою благодарность можно выразить прямиком на банковскую карту (MasterCard): *5169 3600 0134 9707*.
И да, сообщи об этом мне @igorkpl, я сделаю так, что бы тебе никогда не приходила реклама.
Добра тебе. '''
    return bot.send_message(update.message.chat.id, message, parse_mode='Markdown')


def init_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler('start', send_info))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
    dispatcher.add_handler(CallbackQueryHandler(prev_page, True, False, 'pager.prev.*'))
    dispatcher.add_handler(CallbackQueryHandler(next_page, True, False, 'pager.next.*'))
    dispatcher.add_handler(CallbackQueryHandler(download_song, pass_update_queue=True))
    dispatcher.add_handler(CommandHandler('buy', buy))
    dispatcher.add_handler(CommandHandler('donate', donate))
    return dispatcher


if __name__ == '__main__':
    limit = 5
    offset = 0
    search_query = 'hardkiss'

