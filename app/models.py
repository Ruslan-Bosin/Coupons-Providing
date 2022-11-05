from peewee import Model
from peewee import AutoField, CharField, BooleanField, IntegerField, BlobField
from app import db


class BaseModel(Model):
    class Meta:
        database = db


class ClientModel(BaseModel):
    id = AutoField(null=False, primary_key=True)
    name = CharField(null=False)
    email = CharField(null=False, unique=True)
    password = CharField(null=False)
    is_private = BooleanField(default=False)

    class Meta:
        db_table = "clients"

    def to_dict(self):
        return self.__data__


class OrganizationModel(BaseModel):
    id = AutoField(null=False, primary_key=True)
    title = CharField(null=False)
    email = CharField(null=False, unique=True)
    password = CharField(null=False)
    limit = IntegerField(default=10)
    image = BlobField(default='')

    class Meta:
        db_table = "organizations"

    def to_dict(self):
        return self.__data__


def create_tables():
    with db:
        db.create_tables([ClientModel, OrganizationModel])
