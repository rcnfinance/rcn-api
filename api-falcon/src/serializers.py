from graceful.serializers import BaseSerializer
from graceful.fields import RawField
from custom_fields import ListField
from custom_fields import ObjectField


class CommitSerializer(BaseSerializer):
    opcode = RawField("opcode")
    timestamp = RawField("timestamp")
    order = RawField("order")
    proof = RawField("proof")
    data = RawField("data")

class DescriptorSerializer(BaseSerializer):
    firstObligation = RawField("firstObligation")
    totalObligation = RawField("totalObligation")
    duration = RawField("duration")
    interestRate = RawField("interestRate")
    punitiveInterestRate = RawField("punitiveInterestRate")
    frequency = RawField("frecuency")
    installments = RawField("installments")        
        

class DebtSerializer(BaseSerializer):
    id = RawField("id")
    error = RawField("error")
    currency = RawField("currency")
    balance = RawField("balance")
    model = RawField("model")
    creator = RawField("creator")
    oracle = RawField("oracle")
    commits = ListField("list of commits", serializer=CommitSerializer())


class ConfigSerializer(BaseSerializer):
    id = RawField("id")
    data = RawField("data")
    commits = ListField("list of commits", serializer=CommitSerializer())


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
    status = RawField("status")
    commits = ListField("list of commits", serializer=CommitSerializer())

   
class OracleHistorySerializer(BaseSerializer):
    id = RawField("id")
    tokens = RawField("discortokens")
    equivalent = RawField("equivalent")
    timestamp = RawField("timestamp")
