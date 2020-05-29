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
    owner = RawField("owner")


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
    owner = RawField("owner")
    amount = RawField("amount")
    status = RawField("status")

class ConfigSerializer(BaseSerializer):
    id = RawField("id")
    data = RawField("data")


class StateSerializer(BaseSerializer):
    id = RawField("id")
    status = RawField("status")
    clock = RawField("clock")
    last_payment = RawField("last payment")
    paid = RawField("paid")
    paid_base = RawField("paid base")
    interest = RawField("interest")


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
    status = RawField("status")
    canceled = RawField("canceled")


class StateWithoutIDSerializer(BaseSerializer):
    status = RawField("status")
    clock = RawField("clock")
    last_payment = RawField("last payment")
    paid = RawField("paid")
    paid_base = RawField("paid base")
    interest = RawField("interest")


class DebtWithoutIDSerializer(BaseSerializer):
    error = RawField("error")
    balance = RawField("balance")
    model = RawField("model")
    creator = RawField("creator")
    created = RawField("created")
    oracle = RawField("oracle")
    owner = RawField("Owner")


class CollateralWithoutIDSerializer(BaseSerializer):
    id = RawField("id", source="_id")
    oracle = RawField("oracle")
    token = RawField("token")
    amount = RawField("amount")
    liquidation_ratio = RawField("liquidation_ratio")
    balance_ratio = RawField("balance_ratio")
    burn_fee = RawField("burn_fee")
    reward_fee = RawField("reward_fee")
    owner = RawField("owner")
    amount = RawField("amount")
    status = RawField("status")


class CompleteLoanSerializer(BaseSerializer):
    id = RawField("id", source="_id")
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
    status = RawField("status")
    canceled = RawField("canceled")
    debt = ObjectField("debt", serializer=DebtWithoutIDSerializer())
    config = RawField("config")
    state = ObjectField("state", serializer=StateWithoutIDSerializer())
    collaterals = ListField("collaterals", serializer=CollateralWithoutIDSerializer())

class ModelAndDebtSerializer(BaseSerializer):
    due_time = RawField("Due time")
    estimated_obligation = RawField("Estimated Obligation")
    next_obligation = RawField("Next Obligation")
    current_obligation = RawField("Current Obligation")
    debt_balance = RawField("Debt Balance")
    owner = RawField("Owner")
    paid = RawField("Paid")

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
