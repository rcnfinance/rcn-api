from graceful.serializers import BaseSerializer
from graceful.fields import RawField
from custom_fields import ListField
from serializers import CommitSerializer


class ConfigSerializer(BaseSerializer):
    id = RawField("id")
    data = RawField("data")
    commits = ListField("list of commits", serializer=CommitSerializer())
