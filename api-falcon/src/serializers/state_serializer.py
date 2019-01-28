from graceful.serializers import BaseSerializer
from graceful.fields import RawField
from custom_fields import ListField
from serializers import CommitSerializer


class StateSerializer(BaseSerializer):
    id = RawField("id")
    status = RawField("status")
    clock = RawField("clock")
    last_payment = RawField("last payment")
    paid = RawField("paid")
    paid_base = RawField("paid base")
    interest = RawField("interest")
    commits = ListField("List of commits", serializer=CommitSerializer())
