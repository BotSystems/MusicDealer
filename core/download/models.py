import datetime

from peewee import Model, DateTimeField, ForeignKeyField

from core.chanel.models import Chanel
from core.database import db


class Download(Model):
    chanel = ForeignKeyField(Chanel)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
