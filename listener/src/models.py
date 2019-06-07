from mongoengine import StringField
from mongoengine import Document, EmbeddedDocument
from mongoengine import ListField
from mongoengine import IntField
from mongoengine import LongField
from mongoengine import DictField
from mongoengine import EmbeddedDocumentListField
from mongoengine import QuerySet

class Commit(EmbeddedDocument):
    opcode = StringField(required=True, max_length=15)
    timestamp = StringField(required=True)
    order = IntField(required=True)
    proof = StringField(max_length=150)
    data = DictField(required=True)

class Loan(Document):
    index = IntField(required=True, max_length=150, primary_key=True)
    created = StringField(required=True)
    status = IntField(default=0, max_length=150)
    oracle = StringField(required=True, max_length=150)
    borrower = StringField(required=True, max_length=150)
    lender = StringField(default='0x0000000000000000000000000000000000000000', max_length=150)
    creator = StringField(required=True, max_length=150)
    cosigner = StringField(default='0x0000000000000000000000000000000000000000', max_length=150)
    amount = StringField(required=True, max_length=150)
    interest = StringField(default='0', max_length=150)
    punitory_interest = StringField(default='0', max_length=150)
    interest_timestamp = StringField(default='0', max_length=150)
    paid = StringField(default='0', max_length=150)
    interest_rate = StringField(required=True, max_length=150)
    interest_rate_punitory = StringField(required=True, max_length=150)
    due_time = StringField(default='0', max_length=150)
    dues_in = StringField(required=True, max_length=150)
    currency = StringField(required=True, max_length=150)
    cancelable_at = StringField(required=True, max_length=150)
    lender_balance = StringField(default='0', max_length=150)
    expiration_requests = StringField(required=True, max_length=150)
    approved_transfer = StringField(default='0x0000000000000000000000000000000000000000', max_length=150)
    commits = EmbeddedDocumentListField(Commit)
    approbations = ListField(StringField())

class Event(Document):
    uuid = StringField(required=True, max_length=150)

class Schedule(Document):
    opcode = StringField(required=True, max_length=15)
    timestamp = StringField(required=True)
    data = DictField(required=True)

class ClockQuerySet(QuerySet):
    def get_clock(self):
        return self.first()


class ClockModel(Document):
    time = StringField(required=True)

    meta = {'queryset_class': ClockQuerySet}