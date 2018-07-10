from mongoengine import StringField
from mongoengine import Document
from mongoengine import ListField
from mongoengine import IntField


class Loan(Document):
    index = StringField(required=True, max_length=150, primary_key=True)
    created = StringField(required=True, max_length=150)
    status = StringField(default='0', max_length=150)
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
    address = StringField(required=True, max_length=150)
    block_hash = StringField(required=True, max_length=150)
    block_number = IntField(required=True)
    data = StringField(required=True, max_length=300)
    log_index = IntField(required=True, max_length=150)
    topics = ListField(StringField(), required=True)
    transaction_hash = StringField(required=True, max_length=150)
    transaction_index = IntField(required=True, max_length=150)