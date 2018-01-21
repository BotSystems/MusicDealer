from telegram.ext import Dispatcher

from core.bot.models import Bot
from core.handlers.handler import init_handlers


class Factory:
    @staticmethod
    def create(area):
        bot = Bot(area.token)
        bot.area = area
        bot.dispatcher = init_handlers(Dispatcher(bot, None))

        return bot
