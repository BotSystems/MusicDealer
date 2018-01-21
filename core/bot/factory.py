from telegram.ext import Dispatcher
from telegram.ext import messagequeue as mq

from core.bot.models import Bot
from core.handlers.handler import init_handlers


class Factory:
    @staticmethod
    def create(area):
        bot = Bot(area.token)

        bot.area = area
        bot.dispatcher = init_handlers(Dispatcher(bot, None))

        bot._is_messages_queued_default = True
        bot._msg_queue = mq.MessageQueue(25)

        return bot
