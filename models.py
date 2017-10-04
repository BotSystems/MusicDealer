import datetime
import os
from os.path import join, dirname

from dotenv import load_dotenv
from peewee import PostgresqlDatabase, Model, IntegerField, CharField, DateTimeField, ForeignKeyField

if os.path.isfile('.env.settings'):
    dotenv_path = join(dirname(__file__), '.env.settings')
    load_dotenv(dotenv_path)

DATABASE_CREDENTIALS = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host ': os.getenv('DB_HOST'),
    'port ': os.getenv('DB_PORT')
}

db = PostgresqlDatabase(os.getenv('DB_NAME'), **DATABASE_CREDENTIALS)

DEFAULT_LANGUAGE = 'RU'

class Area(Model):
    title = CharField()
    token = CharField(unique=True)
    language = CharField(default=DEFAULT_LANGUAGE)

    class Meta:
        database = db

class Chanel(Model):
    area = ForeignKeyField(Area)

    chanel_id = IntegerField(unique=True)

    first_name = CharField(null=True)
    last_name = CharField(null=True)

    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    def update_me(self):
        self.updated_at = datetime.datetime.now()
        self.save()

    class Meta:
        database = db

class Download(Model):
    chanel = ForeignKeyField(Chanel)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


if __name__ == '__main__':
    pass
