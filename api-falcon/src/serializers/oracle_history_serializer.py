from graceful.serializers import BaseSerializer
from graceful.fields import RawField


class OracleHistorySerializer(BaseSerializer):
    id = RawField("id")
    tokens = RawField("tokens")
    equivalent = RawField("equivalent")
    timestamp = RawField("timestamp")
