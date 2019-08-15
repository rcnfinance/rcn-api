from graceful.serializers import BaseSerializer
from graceful.fields import RawField
from graceful.fields import IntField
from custom_fields import ListField
from custom_fields import ObjectField


class CommitSerializer(BaseSerializer):
    id_loan = RawField("id_loan")
    opcode = RawField("opcode")
    timestamp = RawField("timestamp")
    order = RawField("order")
    proof = RawField("proof")
    address = RawField("address")
    data = RawField("data")


class DescriptorSerializer(BaseSerializer):
    first_obligation = RawField("first_obligation")
    total_obligation = RawField("total_obligation")
    duration = RawField("duration")
    interest_rate = RawField("interest_rate")
    punitive_interest_rate = RawField("punitive_interest_rate")
    frequency = RawField("frecuency")
    installments = RawField("installments")


class DebtSerializer(BaseSerializer):
    id = RawField("id")
    error = RawField("error")
    balance = RawField("balance")
    model = RawField("model")
    creator = RawField("creator")
    created = RawField("created")
    oracle = RawField("oracle")
    # commits = ListField("list of commits", serializer=CommitSerializer())

class CollateralSerializer(BaseSerializer):
    id = RawField("id")
    debt_id = RawField("debt_id")
    oracle = RawField("oracle")
    token = RawField("token")
    amount = RawField("amount")
    liquidation_ratio = RawField("liquidation_ratio")
    balance_ratio = RawField("balance_ratio")
    burn_fee = RawField("burn_fee")
    reward_fee = RawField("reward_fee")
    started = RawField("started")
    invalid = RawField("invalid")
    collateral_ratio = RawField("collateral_ratio")
    can_claim = RawField("can_claim")

class ConfigSerializer(BaseSerializer):
    id = RawField("id")
    data = RawField("data")
    # commits = ListField("list of commits", serializer=CommitSerializer())


class StateSerializer(BaseSerializer):
    id = RawField("id")
    status = RawField("status")
    clock = RawField("clock")
    last_payment = RawField("last payment")
    paid = RawField("paid")
    paid_base = RawField("paid base")
    interest = RawField("interest")
    # commits = ListField("List of commits", serializer=CommitSerializer())


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
    callback = RawField("callback")
    salt = RawField("salt")
    loanData = RawField("loanData")
    created = RawField("created")
    descriptor = ObjectField("descriptor", serializer=DescriptorSerializer())
    currency = RawField("currency")
    lender = RawField("Lender")
    status = RawField("status")
    canceled = RawField("canceled")
    # commits = ListField("list of commits", serializer=CommitSerializer())


class LoanCountSerializer(BaseSerializer):
    count = IntField("Loan count")


class DebtCountSerializer(BaseSerializer):
    count = IntField("Debt count")


class ConfigCountSerializer(BaseSerializer):
    count = IntField("Config count")


class StateCountSerializer(BaseSerializer):
    count = IntField("State count")

class CommitCountSerializer(BaseSerializer):
    count = IntField("State count")

class CollateralCountSerializer(BaseSerializer):
    count = IntField("State count")

class OracleHistorySerializer(BaseSerializer):
    id = RawField("id")
    tokens = RawField("discortokens")
    equivalent = RawField("equivalent")
    timestamp = RawField("timestamp")

class OracleRateSerializer(BaseSerializer):
    oracle = RawField("oracle")
    signer = RawField("signer")
    raw_rate = RawField("raw_rate")
    rate = RawField("rate")
    median_rate = RawField("rate")
    symbol = RawField("symbol")
    timestamp = RawField("timestamp")
    time_bson = RawField("time_bson")

class OracleRateCountSerializer(BaseSerializer):
    count = IntField("Oracle Rate count")
