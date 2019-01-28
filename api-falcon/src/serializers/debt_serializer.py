from graceful.serializers import BaseSerializer
from graceful.fields import RawField
from custom_fields import ListField
from serializers import CommitSerializer


class DebtSerializer(BaseSerializer):
    id = RawField("id")
    error = RawField("error")
    balance = RawField("balance")
    model = RawField("model")
    creator = RawField("creator")
    oracle = RawField("oracle")
    commits = ListField("list of commits", serializer=CommitSerializer())
