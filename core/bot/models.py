import telegram
from telegram.ext import messagequeue as mq


class Bot(telegram.Bot):
    area = None
    dispatcher = None

    '''A subclass of Bot which delegates send method handling to MQ'''

    def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
        super(Bot, self).__init__(*args, **kwargs)
        # below 2 attributes should be provided for decorator usage
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or mq.MessageQueue(25)

    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass
        super(Bot, self).__del__()

    @mq.queuedmessage
    def forward_message(self,
                        chat_id,
                        from_chat_id,
                        message_id,
                        disable_notification=False,
                        timeout=None,
                        **kwargs):
        super(Bot, self).forward_message(chat_id, from_chat_id, message_id, disable_notification, timeout, kwargs)

    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        '''Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments'''
        super(Bot, self).send_message(*args, **kwargs)
