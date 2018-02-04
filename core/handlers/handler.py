# -*- coding: utf-8 -*-

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import MessageHandler, CommandHandler, CallbackQueryHandler, Filters, messagequeue

from core.chanel.models import Chanel
from core.handlers.decorators import save_chanel_decorator
from core.handlers.finder import parse_result, normalize_download_url
from core.handlers.messages import Messages
from core.paging.page import Page

messages = Messages()

PROVIDER_ALIASES = {
    'zaycev_net': 'zn',
    'deezer': 'dz'
}

PROVIDER_ALIASES_BACK = {
    'zn': 'zaycev_net',
    'dz': 'deezer'
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
    messages.set_language(bot.area.language)
    message_id = bot.send_message(update.message.chat.id, messages.get_massage('searching'))
    print('MESSAGE ID: ', message_id)
    # bot.edit_message_text()
    limit, offset = 5, 0
    keyboard = make_markup_keyboard(bot, update.message.chat.id, update.message.text, limit, offset)

    try:
        if keyboard:
            bot.send_message(update.message.chat.id, messages.get_massage('i_find'), reply_markup=keyboard)
        else:
            bot.send_message(update.message.chat.id, messages.get_massage('i_try'))
    except Exception as ex:
        print(ex)


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


def handle_message(bot, update):
    if is_from_group(update):
        broadcast(bot, update)
    else:
        search_track(bot, update)


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
# @save_download_decorator
def download_song(bot, update, *args, **kwargs):
    bot.answer_callback_query(update.callback_query.id, messages.get_massage('download'))
    messages.set_language(bot.area.language)
    query = update.callback_query

    track_link = get_track_link(query.data)
    provider = get_provider_type(query.data)

    download_url = normalize_download_url(track_link, provider)
    bot.send_audio(query.message.chat_id, download_url)


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
    # example_data = '/musicset/play/4ba0a8adb8da96f69b0a8919da9fb0fb/1611152.json'
    #
    # print(get_track_link(example_data))
    # print(get_provider_type(example_data))

    import deezer

    client = deezer.Client()
    track_id = client.search('hardkiss')[0].id
    print(client.get_track(track_id).link)
