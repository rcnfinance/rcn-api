from graceful.serializers import BaseSerializer
from graceful.fields import RawField
from custom_fields import ObjectField
from custom_fields import ListField
from serializers import DescriptorSerializer
from serializers import CommitSerializer


class LoanSerializer(BaseSerializer):
    id = RawField("id")
    open = RawField("open")
    approved = RawField("approved")
    position = RawField("position")
    expiration = RawField("expiration")
    amount = RawField("amount")
    cosigner = RawField("cosigner")
    model = RawField("model")
    creator = RawField("creator")
    oracle = RawField("oracle")
    borrower = RawField("borrower")
    salt = RawField("salt")
    loanData = RawField("loanData")
    created = RawField("created")
    descriptor = ObjectField("descriptor", serializer=DescriptorSerializer())
    currency = RawField("currency")
    lender = RawField("Lender")
    status = RawField("status")
    canceled = RawField("canceled")
    commits = ListField("list of commits", serializer=CommitSerializer())
