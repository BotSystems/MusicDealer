import os
from os.path import join, dirname
from dotenv import load_dotenv

from peewee import PostgresqlDatabase, Model, IntegerField

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


class Chanel(Model):
    chanel_id = IntegerField(unique=True)

    class Meta:
        database = db
