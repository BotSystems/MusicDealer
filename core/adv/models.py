from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class Adv:
    image = None
    link = None
    message = None
    language = None

    def __init__(self, image, link, message):
        self.image = image
        self.link = link
        self.message = message

    def build_keyboard(self, message):
        print(message.get_massage('open_adv'))
        button = [InlineKeyboardButton(message.get_massage('open_adv'), url=self.link)]
        return InlineKeyboardMarkup([button])

    def build_message(self):
        data = [self.message, self.image]
        return '[{}]({})'.format(*data)
