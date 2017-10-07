import os
from os.path import join, dirname
from pathlib import Path

from dotenv import load_dotenv
from peewee import PostgresqlDatabase

setting_path = os.path.join(Path(dirname(__file__)).parent, '.env.local')
if os.path.isfile(setting_path):
    dotenv_path = join(dirname(__file__), setting_path)
    load_dotenv(dotenv_path)

DATABASE_CREDENTIALS = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host ': os.getenv('DB_HOST'),
    'port ': os.getenv('DB_PORT')
}

db = PostgresqlDatabase(os.getenv('DB_NAME'), **DATABASE_CREDENTIALS)
