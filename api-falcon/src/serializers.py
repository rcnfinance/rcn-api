from graceful.serializers import BaseSerializer
from graceful.fields import RawField


class CommitSerializer(BaseSerializer):
    id_loan = RawField("id_loan")
    opcode = RawField("opcode")
    timestamp = RawField("timestamp")
    order = RawField("order")
    proof = RawField("proof")
    data = RawField("data")


class LoanSerializer(BaseSerializer):
    index = RawField('index')
    created = RawField('created')
    status = RawField('status')
    oracle = RawField('oracle')
    borrower = RawField('borrower')
    lender = RawField('lender')
    creator = RawField('creator')
    cosigner = RawField('cosigner')
    amount = RawField('amount')
    interest = RawField('interest')
    punitory_interest = RawField('punitory_interest')
    interest_timestamp = RawField('interest_timestamp')
    paid = RawField('paid')
    interest_rate = RawField('interest_rate')
    interest_rate_punitory = RawField('interest_rate_punitory')
    due_time = RawField('due_time')
    dues_in = RawField('dues_in')
    currency = RawField('currency')
    cancelable_at = RawField('cancelable_at')
    lender_balance = RawField('lender_balance')
    expiration_requests = RawField('expiration_requests')
    approved_transfer = RawField('approved_transfer')
