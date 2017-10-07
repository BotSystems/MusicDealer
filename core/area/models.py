from peewee import Model, CharField

from core.database import db

DEFAULT_LANGUAGE = 'RU'


class Area(Model):
    title = CharField()
    token = CharField(unique=True)
    language = CharField(default=DEFAULT_LANGUAGE)

    class Meta:
        database = db
