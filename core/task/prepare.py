import os

from core.task.task_storages import AmqpStorage

task_storage = AmqpStorage(os.getenv('CLOUDAMQP_URL'))
