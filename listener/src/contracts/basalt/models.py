from mongoengine import StringField
from mongoengine import Document
from mongoengine import ListField
from mongoengine import IntField
from mongoengine import LongField
from mongoengine import EmbeddedDocumentListField
from models import Commit


class Loan(Document):
    index = IntField(required=True, max_length=150, primary_key=True)
    created = LongField(required=True)
    status = IntField(default='0', max_length=150)
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

    def to_dict(self):
        return {
            "index": self.index,
            "created": self.created,
            "status": self.status,
            "amount": self.amount,
            "interest": self.interest,
            "punitory_interest": self.punitory_interest,
            "interest_timestamp": self.interest_timestamp,
            "paid": self.paid,
            "interest_rate": self.interest_rate,
            "interest_rate_punitory": self.interest_rate_punitory,
            "due_time": self.due_time,
            "dues_in": self.dues_in,
            "calcelable_at": self.cancelable_at,
            "expiration_requests": self.expiration_requests
        }

