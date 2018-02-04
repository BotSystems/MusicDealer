class Messages:
    ALL = {
        'ru': {
            'intro': 'Самое время для хорошей музыки. Я уже готов искать твои любимые треки, с чего начнём?',
            'searching': 'Ищу...',
            'i_find': 'Смотри, что я нашел:',
            'i_try': 'Я действительно старался, но нет ничего :(',
            'open_adv': 'Открыть',
            'download': '🔊 Загрузка...'
        },
        'en': {
            'intro': 'It`s time for good music. I`m ready to search for your favorite tracks, where do we start?',
            'searching': 'Searching...',
            'i_find': 'Check this sounds, bro:',
            'i_try': 'I really tried but i can`t find anything :(',
            'open_adv': 'Open',
            'download': '🔊 Download...'
        }
    }
    DEFAULT_LANGUAGE = 'ru'

    language = DEFAULT_LANGUAGE

    def set_language(self, language):
        accepted_language = ('ru', 'en')
        language = language.lower()
        self.language = language if language in accepted_language else self.DEFAULT_LANGUAGE

    def get_massage(self, alias):
        return self.ALL[self.language][alias]


if __name__ == '__main__':
    language_processor = Messages()

    language_processor.set_language('ru')
    print(language_processor.get_massage('i_find'))

    language_processor.set_language('en')
    print(language_processor.get_massage('i_find'))
