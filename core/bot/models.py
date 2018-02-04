import telegram
from telegram.ext import messagequeue as mq


class Bot(telegram.Bot):
    area = None
    dispatcher = None

    _is_messages_queued_default = None
    _msg_queue = None

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
        super(Bot, self).forward_message(chat_id, from_chat_id, message_id, disable_notification, timeout, **kwargs)
