import datetime

from peewee import Model, IntegerField, CharField, DateTimeField, ForeignKeyField

from core.area.models import Area
from core.database import db


class Chanel(Model):
    area = ForeignKeyField(Area)

    chanel_id = IntegerField()

    first_name = CharField(null=True)
    last_name = CharField(null=True)

    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    def update_me(self):
        self.updated_at = datetime.datetime.now()
        self.save()

    class Meta:
        database = db
