from mongoengine import StringField
from mongoengine import Document, EmbeddedDocument
from mongoengine import IntField
from mongoengine import LongField
from mongoengine import DictField
from mongoengine import ListField
from mongoengine import BooleanField
from mongoengine import QuerySet


class Commit(EmbeddedDocument):
    opcode = StringField(required=True, max_length=15)
    timestamp = LongField(required=True)
    order = IntField(required=True)
    proof = StringField(required=True, max_length=150)
    data = DictField(required=True)

class Debt(Document):
    id = StringField(required=True, max_length=150, primary_key=True)
    error = BooleanField()
    currency = StringField(required=True, max_length=150)
    balance = StringField(required=True, max_length=150)
    model = StringField(required=True, max_length=150)
    creator = StringField(required=True, max_length=150)
    oracle = StringField(required=True, max_length=150)

    config = DictField()
    states = ListField()


class ClockQuerySet(QuerySet):
    def get_clock(self):
        return self.first()


class ClockModel(Document):
    time = StringField(required=True)

    meta = {'queryset_class': ClockQuerySet}