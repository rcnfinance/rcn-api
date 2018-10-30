from graceful.serializers import BaseSerializer
from graceful.fields import RawField
from custom_fields import ListField


class CommitSerializer(BaseSerializer):
    opcode = RawField("opcode")
    timestamp = RawField("timestamp")
    order = RawField("order")
    proof = RawField("proof")
    data = RawField("data")

class DebtSerializer(BaseSerializer):
    id = RawField("id")
    error = RawField("error")
    currency = RawField("currency")
    balance = RawField("balance")
    model = RawField("model")
    creator = RawField("creator")
    oracle = RawField("oracle")

