import os
from functools import partial

MESSAGES = {
    'RU': {
        'intro': 'Отправь мне имя исполнителя, либо название песни и я постараюсь её найти. Автор бота: @igorkpl.',
        'searching': 'Ищу...',
        'i_find': 'Смотри, что я нашел:',
        'i_try': 'Я действительно старался, но нет ничего :('
    },
    'EN': {
        'intro': 'I can find and send audio file for you, if you tell me what I need to find :)',
        'searching': 'Searching...',
        'i_find': 'Check this sounds, bro:',
        'i_try': 'I really tried but i can`t find anything :('
    }
}

selected_language = os.getenv('LANGUAGE', 'EN')


def get_message(language, messages, key):
    return messages[language][key]


get_message_by_key = partial(partial(get_message, selected_language), MESSAGES)
