from graceful.serializers import BaseSerializer
from graceful.fields import RawField


class DescriptorSerializer(BaseSerializer):
    first_obligation = RawField("first_obligation")
    total_obligation = RawField("total_obligation")
    duration = RawField("duration")
    interest_rate = RawField("interest_rate")
    punitive_interest_rate = RawField("punitive_interest_rate")
    frequency = RawField("frecuency")
    installments = RawField("installments")
