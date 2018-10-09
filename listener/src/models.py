from mongoengine import StringField
from mongoengine import LongField
from mongoengine import DictField
from mongoengine import IntField
from mongoengine import Document
from mongoengine import QuerySet
from mongoengine import EmbeddedDocument


class Commit(EmbeddedDocument):
    opcode = StringField(required=True, max_length=15)
    timestamp = LongField(required=True)
    order = IntField(required=True)
    proof = StringField(max_length=150)
    data = DictField(required=True)

class Schedule(Document):
    opcode = StringField(required=True, max_length=15)
    timestamp = LongField(required=True)
    data = DictField(required=True)

class ClockQuerySet(QuerySet):
    def get_clock(self):
        return self.first()


class ClockModel(Document):
    time = StringField(required=True)

    meta = {'queryset_class': ClockQuerySet}