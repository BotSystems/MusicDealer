from peewee import Model
from peewee import Model, IntegerField, CharField, DateTimeField, ForeignKeyField, BooleanField
from core.database import db


# Storage
class Storage(Model):
    type = CharField(null=True)
    is_group = BooleanField()
    name = CharField(null=True)
    id = IntegerField()

    class Meta:
        database = db


# StorageDownloadLink

# StorageDownload

# StorageDownloadResult


if __name__ == '__main__':
    pass
