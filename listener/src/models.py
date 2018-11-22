from mongoengine import StringField
from mongoengine import LongField
from mongoengine import DictField
from mongoengine import BooleanField
from mongoengine import IntField
from mongoengine import Document
from mongoengine import QuerySet
from mongoengine import EmbeddedDocument
from mongoengine import EmbeddedDocumentListField


class Commit(EmbeddedDocument):
    opcode = StringField(required=True, max_length=50)
    timestamp = LongField(required=True)
    order = IntField(required=True)
    proof = StringField(max_length=150)
    data = DictField(required=True)


class Schedule(Document):
    opcode = StringField(required=True, max_length=50)
    timestamp = LongField(required=True)
    data = DictField(required=True)


class ClockQuerySet(QuerySet):
    def get_clock(self):
        return self.first()


class ClockModel(Document):
    time = StringField(required=True)
    meta = {'queryset_class': ClockQuerySet}


class Config(Document):
    id = StringField(required=True, max_length=150, primary_key=True)
    data = DictField()
    commits = EmbeddedDocumentListField(Commit)


class Debt(Document):
    id = StringField(required=True, max_length=150, primary_key=True)
    error = BooleanField()
    currency = StringField(required=True, max_length=150)
    balance = StringField(required=True, max_length=150)
    model = StringField(required=True, max_length=150)
    creator = StringField(required=True, max_length=150)
    oracle = StringField(required=True, max_length=150)
    created = StringField(required=True, max_length=100)
    commits = EmbeddedDocumentListField(Commit)


class Request(Document):
    id = StringField(required=True, max_length=150, primary_key=True)
    open = BooleanField(required=True)
    approved = BooleanField(required=True)
    position = StringField(required=True, max_length=150)
    expiration = StringField(required=True, max_length=150)
    amount = StringField(required=True, max_length=150)
    cosigner = StringField(required=True, max_length=150)
    model = StringField(required=True, max_length=150)
    creator = StringField(required=True, max_length=150)
    oracle = StringField(required=True, max_length=150)
    borrower = StringField(required=True, max_length=150)
    salt = StringField(required=True, max_length=150)
    loanData = StringField(required=True, max_length=150)
    canceled = BooleanField(default=False)
    created = StringField(required=True, max_length=100)
    commits = EmbeddedDocumentListField(Commit)


class OracleHistory(Document):
    id = StringField(required=True, max_length=150, primary_key=True)
    tokens = StringField(required=True, max_length=150)
    equivalent = StringField(required=True, max_length=150)
    timestamp = StringField(required=True, max_length=100)
