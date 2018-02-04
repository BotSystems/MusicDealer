from telegram.bot import Bot
from telegram.ext import messagequeue as mq


class MQBot(Bot):
    area = None
    dispatcher = None

    # _is_messages_queued_default = None
    # _msg_queue = None

    def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
        super(MQBot, self).__init__(*args, **kwargs)
        # below 2 attributes should be provided for decorator usage
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or mq.MessageQueue()

    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass
        super(MQBot, self).__del__()

    @mq.queuedmessage
    def forward_message(self,
                        chat_id,
                        from_chat_id,
                        message_id,
                        disable_notification=False,
                        timeout=None,
                        **kwargs):
        super(MQBot, self).forward_message(chat_id, from_chat_id, message_id, disable_notification, timeout, **kwargs)
