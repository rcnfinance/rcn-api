import os

from mongoengine import StringField
from mongoengine import LongField
from mongoengine import DictField
from mongoengine import BooleanField
from mongoengine import IntField
from mongoengine import Document
from mongoengine import QuerySet
from mongoengine import EmbeddedDocument
from mongoengine import EmbeddedDocumentField
from mongoengine import connect

connect(db=os.environ.get("MONGO_DB", "rcn"), host=os.environ.get("MONGO_HOST", "localhost"))


class Commit(Document):
    id_loan = StringField(required=False, max_length=150)
    opcode = StringField(required=True, max_length=50)
    timestamp = LongField(required=True)
    order = IntField(required=True)
    proof = StringField(max_length=150)
    data = DictField(required=True)
    address = StringField(required=True, max_length=150)

    meta = {
        "indexes": [
            "id_loan",
            "proof",
            "address"
        ]
    }


class Descriptor(EmbeddedDocument):
    first_obligation = StringField(required=True, max_length=150)
    total_obligation = StringField(required=True, max_length=150)
    duration = StringField(required=True, max_length=150)
    interest_rate = StringField(required=True, max_length=150)
    punitive_interest_rate = StringField(required=True, max_length=150)
    frequency = StringField(required=True, max_length=150)
    installments = StringField(required=True, max_length=150)


class Config(Document):
    id = StringField(required=True, max_length=150, primary_key=True)
    data = DictField()


class State(Document):
    id = StringField(required=True, max_length=150, primary_key=True)
    status = StringField(max_length=2, default="0")
    clock = StringField(required=True, max_length=100)
    last_payment = StringField(max_length=100, default="0")
    paid = StringField(max_length=100, default="0")
    paid_base = StringField(max_length=100, default="0")
    interest = StringField(max_length=100, default="0")

    meta = {
        "indexes": [
            "status"
        ]
    }


class Debt(Document):
    id = StringField(required=True, max_length=150, primary_key=True)
    error = BooleanField()
    balance = StringField(required=True, max_length=150)
    model = StringField(required=True, max_length=150)
    creator = StringField(required=True, max_length=150)
    oracle = StringField(required=True, max_length=150)
    created = StringField(required=True, max_length=100)

    meta = {
        "indexes": [
            "error",
            "model",
            "creator",
            "oracle",
            "balance",
            "created"
        ]
    }


class Loan(Document):
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
    created = StringField(required=True, max_length=100)
    descriptor = EmbeddedDocumentField(Descriptor)
    currency = StringField(required=True, max_length=150)
    status = StringField(required=True, max_length=150)
    canceled = BooleanField(default=False)
    lender = StringField(required=False, max_length=150)

    meta = {
        "indexes": [
            "open",
            "approved",
            "cosigner",
            "model",
            "creator",
            "oracle",
            "borrower",
            "expiration",
            "amount"
        ]
    }
