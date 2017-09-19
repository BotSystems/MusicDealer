import os
from functools import partial

MESSAGES = {
    'RU': {
        'intro': 'Самое время для хорошей музыки. Я уже готов искать твои любимые треки, с чего начнём?',
        'searching': 'Ищу...',
        'i_find': 'Смотри, что я нашел:',
        'i_try': 'Я действительно старался, но нет ничего :('
    },
    'EN': {
        'intro': 'It`s time for good music. I`m ready to search for your favorite tracks, where do we start?',
        'searching': 'Searching...',
        'i_find': 'Check this sounds, bro:',
        'i_try': 'I really tried but i can`t find anything :('
    }
}

selected_language = os.getenv('LANGUAGE', 'EN')


def get_message(language, messages, key):
    return messages[language][key]


get_message_by_key = partial(partial(get_message, selected_language), MESSAGES)
