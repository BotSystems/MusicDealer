import telegram


class Bot(telegram.Bot):
    area = None
    dispatcher = None

    def add_area(self, area):
        self.area = area

    def add_dispatcher(self, dispatcher):
        self.dispatcher = dispatcher
