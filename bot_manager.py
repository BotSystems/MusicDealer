import telegram

class Bot(telegram.Bot):
    dispatcher = None

    def add_dispatcher(self, dispatcher):
        self.dispatcher = dispatcher

# class BotManager:
#     bots