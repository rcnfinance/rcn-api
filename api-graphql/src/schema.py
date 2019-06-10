import graphene

from models import Debt as DebtModel
from models import Loan as LoanModel
from models import State as StateModel
from models import Config as ConfigModel
from models import Commit as CommitModel

from utils import get_data


class Commit(graphene.ObjectType):
    id_loan = graphene.String()
    opcode = graphene.String()
    timestamp = graphene.Int()
    order = graphene.Int()
    proof = graphene.String()
    data = graphene.JSONString()
    address = graphene.String()


class Descriptor(graphene.ObjectType):
    first_obligation = graphene.String()
    total_obligation = graphene.String()
    duration = graphene.String()
    interest_rate = graphene.String()
    punitive_interest_rate = graphene.String()
    frequency = graphene.String()
    installments = graphene.String()


class ModelDebtInfo(graphene.ObjectType):
    paid = graphene.String(name="paid")
    due_time = graphene.String(name="due_time")
    estimated_obligation = graphene.String(name="estimated_obligation")
    next_obligation = graphene.String(name="next_obligation")
    current_obligation = graphene.String(name="current_obligation")
    debt_balance = graphene.String(name="debt_balance")
    owner = graphene.String(name="owner")


def resolve(debt, info, **args):
    data = get_data(debt.id)
    return ModelDebtInfo(**data)


class Debt(graphene.ObjectType):
    id = graphene.ID()
    error = graphene.Boolean()
    balance = graphene.String()
    model = graphene.String()
    creator = graphene.String()
    oracle = graphene.String()
    created = graphene.String()
    modeldebtinfo = graphene.Field(ModelDebtInfo, resolver=resolve)


class Loan(graphene.ObjectType):
    id = graphene.ID()
    open = graphene.Boolean()
    approved = graphene.Boolean()
    position = graphene.String()
    expiration = graphene.String()
    amount = graphene.String()
    cosigner = graphene.String()
    model = graphene.String()
    creator = graphene.String()
    oracle = graphene.String()
    borrower = graphene.String()
    salt = graphene.String()
    loanData = graphene.String()
    created = graphene.String()
    descriptor = graphene.Field(Descriptor)
    currency = graphene.String()
    status = graphene.String()
    canceled = graphene.Boolean()
    lender = graphene.String()


class State(graphene.ObjectType):
    id = graphene.ID()
    status = graphene.String()
    clock = graphene.String()
    last_payment = graphene.String()
    paid = graphene.String()
    paid_base = graphene.String()
    interest = graphene.String()


class Config(graphene.ObjectType):
    id = graphene.ID()
    data = graphene.JSONString()


class Query(graphene.ObjectType):
    modeldebtinfo = graphene.Field(ModelDebtInfo,
        id=graphene.ID(required=True)
    )

    debt = graphene.List(Debt, 
        id=graphene.ID(required=False),
        error=graphene.Boolean(required=False),
        model=graphene.String(required=False),
        creator=graphene.String(required=False),
        oracle=graphene.String(required=False),

        first=graphene.Int(required=False),
        skip=graphene.Int(required=False),

        balance__gt=graphene.String(required=False, name="balance__gt"),
        balance__gte=graphene.String(required=False, name="balance__gte"),
        balance__lt=graphene.String(required=False, name="balance__lt"),
        balance__lte=graphene.String(required=False, name="balance__lte"),

        created__gt=graphene.String(required=False, name="created__gt"),
        created__gte=graphene.String(required=False, name="created__gte"),
        created__lt=graphene.String(required=False, name="created__lt"),
        created__lte=graphene.String(required=False, name="created__lte"),
    )

    config = graphene.List(Config, id=graphene.ID(required=False))

    state = graphene.List(State, 
        id=graphene.ID(required=False),
        status=graphene.String(required=False),

        first=graphene.Int(required=False),
        skip=graphene.Int(required=False)
    )

    loan = graphene.List(Loan,
        id=graphene.ID(required=False),
        open=graphene.Boolean(required=False),
        approved=graphene.Boolean(required=False),
        cosigner=graphene.String(required=False),
        model=graphene.String(required=False),
        creator=graphene.String(required=False),
        oracle=graphene.String(required=False),
        borrower=graphene.String(required=False),
        currency=graphene.String(required=False),
        status=graphene.String(required=False),
        canceled=graphene.Boolean(required=False),
        lender=graphene.String(required=False),

        first=graphene.Int(required=False),
        skip=graphene.Int(required=False),

        expiration__gt=graphene.String(required=False, name="expiration__gt"),
        expiration__gte=graphene.String(required=False, name="expiration__gte"),
        expiration__t=graphene.String(required=False, name="expiration__lt"),
        expiration__lte=graphene.String(required=False, name="expiration__lte"),

        amount__gt=graphene.String(required=False, name="amount__gt"),
        amount__gte=graphene.String(required=False, name="amount__gte"),
        amount__lt=graphene.String(required=False, name="amount__lt"),
        amount__lte=graphene.String(required=False, name="amount__lte"),

        created__gt=graphene.String(required=False, name="created__gt"),
        created__gte=graphene.String(required=False, name="created__gte"),
        created__lt=graphene.String(required=False, name="created__lt"),
        created__lte=graphene.String(required=False, name="created__lte"),
    )

    commit = graphene.List(Commit,
        id_loan=graphene.ID(required=False),
        opcode=graphene.String(required=False),
        proof=graphene.String(required=False),
        address=graphene.String(required=False),

        first=graphene.Int(required=False),
        skip=graphene.Int(required=False)
    )

    def resolve_modeldebtinfo(root, info, id):
        data = get_data(id)
        return ModelDebtInfo(**data)

    def resolve_debt(root, info, **args):
        first = args.get("first", 10)
        skip = args.get("skip", 0)
        if "first" in args:
            del args["first"]
        if "skip" in args:
            del args["skip"]
        return DebtModel.objects.filter(**args).skip(skip).limit(first)

    def resolve_config(root, info, **args):
        return ConfigModel.objects.filter(**args)

    def resolve_state(root, info, **args):
        first = args.get("first", 10)
        skip = args.get("skip", 0)
        if "first" in args:
            del args["first"]
        if "skip" in args:
            del args["skip"]
        return StateModel.objects.filter(**args).skip(skip).limit(first)

    def resolve_loan(root, info, **args):
        first = args.get("first", 10)
        skip = args.get("skip", 0)
        if "first" in args:
            del args["first"]
        if "skip" in args:
            del args["skip"]
        return LoanModel.objects.filter(**args).skip(skip).limit(first)

    def resolve_commit(root, info, **args):
        first = args.get("first", 10)
        skip = args.get("skip", 0)
        if "first" in args:
            del args["first"]
        if "skip" in args:
            del args["skip"]
        return CommitModel.objects.filter(**args).skip(skip).limit(first)


schema = graphene.Schema(query=Query, types=[Debt, ])
