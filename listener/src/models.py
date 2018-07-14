from mongoengine import StringField
from mongoengine import Document
from mongoengine import ListField
from mongoengine import IntField
from mongoengine import LongField
from mongoengine import BooleanField
from mongoengine import DictField

class Loan(Document):
    index = IntField(required=True, max_length=150, primary_key=True)
    created = LongField(required=True)
    status = IntField(default='0', max_length=150)
    oracle = StringField(required=True, max_length=150)
    borrower = StringField(required=True, max_length=150)
    lender = StringField(default='0x0', max_length=150)
    creator = StringField(required=True, max_length=150)
    cosigner = StringField(default='0x0', max_length=150)
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
    approved_transfer = StringField(default='0x0', max_length=150)

class Event(Document):
    uuid = StringField(required=True, max_length=150)

class Commit(Document):
    opcode = StringField(required=True, max_length=15)
    timestamp = LongField(required=True)
    order = IntField(required=True)
    proof = StringField(required=True, max_length=150)
    data = DictField(required=True)
    executed = BooleanField(default=False)