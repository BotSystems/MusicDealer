# -*- coding: utf-8 -*-
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import MessageHandler, CommandHandler, CallbackQueryHandler
from handlers.messages import get_message_by_key
import json
import os.path

#
# SCHEMA_FILENAME = os.path.join(os.path.dirname(__file__), 'data', 'menu.json')
# CALLBACKS_FILENAME = os.path.join(os.path.dirname(__file__), 'data', 'callback.json')
#
#
# def get_menu_schema():
#     with open(SCHEMA_FILENAME, encoding='utf8') as f:
#         return json.load(f)
#
#
# def create_menu_item(item_settings):
#     # Пока создаём только инлайн кнопки
#     text = item_settings['title']
#     callback_data = item_settings['callback']
#     url = item_settings['link']
#     return InlineKeyboardButton(text=text, url=url, callback_data=callback_data)
#
#
# def render_menu_schema(menu_schema):
#     menu = []
#     for item_schema in menu_schema['menu']:
#         item = create_menu_item(item_schema)
#         menu.append([item])
#     return menu
#
#
# def build_keyboard():
#     menu_schema = get_menu_schema()
#     menu = render_menu_schema(menu_schema)
#     markup = InlineKeyboardMarkup(menu)
#     return markup
#
#
# def show_menu(bot, update):
#     markup = build_keyboard()
#     bot.send_message(update.message.chat.id, 'Пройдите курс обучение и начните зарабатывать.', reply_markup=markup)
#
#
# def render_to_markdown(callback_data_answer):
#     template = '*{}*\n{}\n[>> СМОТРЕТЬ <<]({})'
#     return template.format(callback_data_answer['title'], callback_data_answer['description'],
#                            callback_data_answer['video'])
#
#
# def menu_item_handler(bot, update):
#     callback = update.callback_query.data
#     with open(CALLBACKS_FILENAME, encoding='utf8') as f:
#         callback_answers = json.load(f)
#         if callback in callback_answers:
#             result = render_to_markdown(callback_answers[callback])
#             bot.send_message(update.callback_query.message.chat.id, result, parse_mode='Markdown',
#                              reply_markup=build_keyboard())
#
from handlers.decorators import save_chanel_decorator
from handlers.finder import parse_result, normalize_song_name, normalize_download_url


def build_download_keyboard(songs_data):
    download_buttons = []
    for title, url in songs_data:
        inline_download_button = InlineKeyboardButton(title, callback_data=url)
        download_buttons.append([inline_download_button])
    return download_buttons


@save_chanel_decorator
def search_audio(bot, update):
    try:
        bot.send_message(update.message.chat.id, get_message_by_key('searching'))
        songs_data = parse_result(normalize_song_name(update.message.text))
        songs_data = list(filter(None, songs_data))
        # download_urls = [get_download_urls(url) for url in songs_data]
        buttons = build_download_keyboard(songs_data)
        keyboard = InlineKeyboardMarkup(buttons)

        if buttons:
            bot.send_message(update.message.chat.id, get_message_by_key('i_find'), reply_markup=keyboard)
        else:
            bot.send_message(update.message.chat.id, get_message_by_key('i_try'))
    except Exception as ex:
        print(ex)


@save_chanel_decorator
def send_info(bot, update):
    message = get_message_by_key('intro')
    # message = 'I can find and send audio file for you, if you tell me what I need to find :)'
    bot.send_message(update.message.chat.id, message)

@save_chanel_decorator
def download_song(bot, update, *args, **kwargs):
    query = update.callback_query
    # print(update)
    download_url = normalize_download_url(query.data)
    bot.send_audio(query.message.chat_id, download_url)


def init_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler('start', send_info))
    dispatcher.add_handler(MessageHandler(None, search_audio))
    dispatcher.add_handler(CallbackQueryHandler(download_song, pass_update_queue=True))
    return dispatcher
