# -*- coding: utf-8 -*-
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import MessageHandler, CommandHandler, CallbackQueryHandler, Filters, BaseFilter

from core.adv.controller import send_adv
from core.handlers.decorators import save_chanel_decorator, save_download_decorator
from core.handlers.finder import parse_result, normalize_download_url
from core.handlers.messages import Messages
from core.paging.page import Page

messages = Messages()

BOTONARIOUM = '::Ботонариум::'


# def _build_botonarioum_keyboard(bot, update):
#     area = Area.get(Area.token == bot.area.token)
#     if (area.language in ('RU')):
#         buttons = [[BOTONARIOUM]]
#         keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
#         bot.send_message(update.message.chat.id, messages.get_massage('i_find'), reply_markup=keyboard)


def build_download_keyboard(songs_data):
    download_buttons = []
    for title, url in songs_data:
        inline_download_button = InlineKeyboardButton(title, callback_data=url)
        download_buttons.append([inline_download_button])
    return download_buttons


@save_chanel_decorator
def send_botonarioum_info(bot, update):
    print('ok1')
    message = 'Ботонариум - вселенная, где обитают боты.'
    print('ok2')
    button = [[InlineKeyboardButton('Присоединиться', url='https://t.me/botonarioum')]]
    print('ok3')
    return bot.send_message(update.message.chat.id, message, reply_markup=InlineKeyboardMarkup(button))


class BotonarioumFilter(BaseFilter):
    def filter(self, message):
        return bool(message.text == BOTONARIOUM)


def attach_pager_buttons(buttons, pager, song_name):
    limit, offset = pager.limit, pager.offset
    pagination_buttons = [[]]

    if pager.has_next:
        pagination_buttons[0].append(InlineKeyboardButton('>>>', callback_data='pager.next.limit.{}.offset.{}.track_name.{}'.format(limit, offset, song_name)))

    if pager.has_prev:
        pagination_buttons[0].append(InlineKeyboardButton('<<<', callback_data='pager.prev.limit.{}.offset.{}.track_name.{}'.format(limit, offset, song_name)))

    return pagination_buttons + buttons + pagination_buttons


@save_chanel_decorator
def search_audio(bot, update):
    messages.set_language(bot.area.language)
    bot.send_message(update.message.chat.id, messages.get_massage('searching'))
    limit, offset = 10, 0
    keyboard = make_markup_keyboard(bot, update.message.chat.id, update.message.text, limit, offset)
    if keyboard:
        bot.send_message(update.message.chat.id, messages.get_massage('i_find'), reply_markup=keyboard)
    else:
        bot.send_message(update.message.chat.id, messages.get_massage('i_try'))

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
            # bot.send_message(chat_id, messages.get_massage('i_find'), reply_markup=keyboard)
        # else:

            # bot.send_message(chat_id, messages.get_massage('i_try'))
    except Exception as ex:
        print(ex)
    return None

# def searching(bot, chat_id, text, limit, offset):
#
#
#     print('limit: {}'.format(limit))
#     print('offset: {}'.format(offset))
#
#     try:
#         print('1')
#         # print('1')
#         # bot.send_message(update.message.chat.id, messages.get_massage('searching'))
#
#         print('2')
#
#         songs_data, songs_count = parse_result(text, limit, offset)
#         songs_data = list(filter(None, songs_data))
#
#         pager = Page(songs_count, limit, offset)
#
#         songs_buttons = build_download_keyboard(songs_data)
#
#         if songs_buttons:
#             buttons = attach_pager_buttons(songs_buttons, pager, text)
#             keyboard = InlineKeyboardMarkup(buttons)
#             bot.send_message(chat_id, messages.get_massage('i_find'), reply_markup=keyboard)
#         else:
#             bot.send_message(chat_id, messages.get_massage('i_try'))
#     except Exception as ex:
#         print(ex)


def next_page(bot, update, *args, **kwargs):
    query = update.callback_query

    limit = int(query.data.split('.')[3])
    offset = int(query.data.split('.')[5])
    song_name = query.data.split('.')[7]

    print(update.callback_query.message.chat_id)
    print(update.callback_query.message.message_id)

    keyboard = make_markup_keyboard(bot, update.callback_query.message.chat_id, song_name, limit, offset - limit)
    bot.edit_message_reply_markup(update.callback_query.message.chat_id, update.callback_query.message.message_id, None, keyboard)
    # bot.edit_message_text('aaaaaaaaaaaaaa', update.callback_query.message.chat_id, update.callback_query.message.message_id)
    # query = update.callback_query
    # print(query)
    # limit = int(query.data.split('.')[3])
    # offset = int(query.data.split('.')[5])
    # song_name = query.data.split('.')[7]
    # print('next page')
    # print(update)
    # searching(bot, query.message.chat_id, song_name, limit, offset + limit)

def prev_page(bot, update, *args, **kwargs):
    query = update.callback_query
    print(query)
    limit = int(query.data.split('.')[3])
    offset = int(query.data.split('.')[5])
    song_name = query.data.split('.')[7]
    print('prev page')
    print(update)
    make_markup_keyboard(bot, query.message.chat_id, song_name, limit, offset - limit)

@save_chanel_decorator
def send_info(bot, update):
    messages.set_language(bot.area.language)
    message = messages.get_massage('intro')
    # area = Area.get(Area.token == bot.area.token)
    # if (area.language in ('RU')):
    #     buttons = [[BOTONARIOUM]]
    #     keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    #     return bot.send_message(update.message.chat.id, message, reply_markup=keyboard)
    return bot.send_message(update.message.chat.id, message)


@save_chanel_decorator
# @save_download_decorator
def download_song(bot, update, *args, **kwargs):
    messages.set_language(bot.area.language)
    query = update.callback_query
    download_url = normalize_download_url(query.data)
    bot.send_audio(query.message.chat_id, download_url)
    # send_adv(bot, query.message.chat_id, messages)


def init_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler('start', send_info))
    dispatcher.add_handler(MessageHandler(BotonarioumFilter(), send_botonarioum_info))
    dispatcher.add_handler(MessageHandler(Filters.text, search_audio))
    dispatcher.add_handler(CallbackQueryHandler(prev_page, True, False, 'pager.prev.*'))
    dispatcher.add_handler(CallbackQueryHandler(next_page, True, False, 'pager.next.*'))
    dispatcher.add_handler(CallbackQueryHandler(download_song, pass_update_queue=True))
    return dispatcher


if __name__ == '__main__':
    pass
