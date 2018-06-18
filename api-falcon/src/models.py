from mongoengine import StringField
from mongoengine import Document


class Loan(Document):
    index = StringField(required=True, max_length=150, primary_key=True)
    created = StringField(required=True, max_length=150)
    status = StringField(required=True, max_length=150)
    oracle = StringField(required=True, max_length=150)
    borrower = StringField(required=True, max_length=150)
    lender = StringField(required=True, max_length=150)
    creator = StringField(required=True, max_length=150)
    cosigner = StringField(required=True, max_length=150)
    amount = StringField(required=True, max_length=150)
    interest = StringField(required=True, max_length=150)
    punitory_interest = StringField(required=True, max_length=150)
    interest_timestamp = StringField(required=True, max_length=150)
    paid = StringField(required=True, max_length=150)
    interest_rate = StringField(required=True, max_length=150)
    interest_rate_punitory = StringField(required=True, max_length=150)
    due_time = StringField(required=True, max_length=150)
    dues_in = StringField(required=True, max_length=150)
    currency = StringField(required=True, max_length=150)
    cancelable_at = StringField(required=True, max_length=150)
    lender_balance = StringField(required=True, max_length=150)
    expiration_requests = StringField(required=True, max_length=150)