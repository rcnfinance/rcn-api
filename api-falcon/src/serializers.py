from graceful.serializers import BaseSerializer
from graceful.fields import RawField
from custom_fields import ListField


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
    descriptor = ListField("descriptor", serializer=DescriptorSerializer())
    currency = RawField("currency")
    status = RawField("status")
    commits = ListField("list of commits", serializer=CommitSerializer())

   
class OracleHistorySerializer(BaseSerializer):
    id = RawField("id")
    tokens = RawField("discortokens")
    equivalent = RawField("equivalent")
    timestamp = RawField("timestamp")



class DescriptorSerializer(BaseSerializer):
    firstObligation = RawField("firstObligation")
    totalObligation = RawField("totalObligation")
    duration = RawField("duration")
    interestRate = RawField("interestRate")
    punitiveInterestRate = RawField("punitiveInterestRate")
    frequency = RawField("frecuency")
    installments = RawField("installments")        

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
    descriptor = ListField("descriptor", serializer=DescriptorSerializer())
    currency = RawField("currency")
    status = RawField("status")
    commits = ListField("list of commits", serializer=CommitSerializer())    
        


class LoanList(PaginatedListAPI):
    serializer = LoanSerializer()

    open = BoolParam("Open filter")
    approved = BoolParam("Approved filter")
    cosigner = StringParam("Cosigner filter")
    model = StringParam("Model filter")
    creator = StringParam("Creator filter")
    oracle = StringParam("Oracle filter")
    borrower = StringParam("Borrower filter")
    canceled = StringParam("Canceled filter")

    def list(self, params, meta, **kwargs):
        # Filtering -> Ordering -> Limiting
        filter_params = params.copy()
        filter_params.pop("indent")

        page_size = filter_params.pop("page_size")
        page = filter_params.pop("page")

        offset = page * page_size

        return Loan.objects.filter(**filter_params).skip(offset).limit(page_size)        