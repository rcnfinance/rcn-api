import logging
import time
import json
from graceful.resources.generic import RetrieveAPI
from graceful.resources.generic import PaginatedListAPI
from graceful.parameters import StringParam
from graceful.parameters import BoolParam
import falcon
from serializers import DebtSerializer
from serializers import ConfigSerializer
from serializers import LoanSerializer
from serializers import EntrySerializer
from serializers import OracleHistorySerializer
from serializers import StateSerializer
from serializers import LoanCountSerializer
from serializers import EntryCountSerializer
from serializers import DebtCountSerializer
from serializers import ConfigCountSerializer
from serializers import StateCountSerializer
from serializers import CommitSerializer
from serializers import CommitCountSerializer
from models import Debt
from models import Config
from models import Loan
from models import Entry
from models import OracleHistory
from models import State
from models import Commit
from clock import Clock
from utils import get_data


logger = logging.getLogger(__name__)


class DebtList(PaginatedListAPI):
    serializer = DebtSerializer()

    error = BoolParam("Error filter")
    model = StringParam("Model filter")
    creator = StringParam("Creator filter")
    oracle = StringParam("Oracle filter")

    balance__lt = StringParam("Balance lt")
    balance__lte = StringParam("Balance lte")
    balance__gt = StringParam("Balance gt")
    balance__gte = StringParam("Balance gte")

    created__lt = StringParam("Created lt")
    created__lte = StringParam("Created lt")
    created__gt = StringParam("Created gt")
    created__gte = StringParam("Created gte")

    def list(self, params, meta, **kwargs):
        # Filtering -> Ordering -> Limiting

        filter_params = params.copy()
        filter_params.pop("indent")

        page_size = filter_params.pop("page_size")
        page = filter_params.pop("page")

        offset = page * page_size

        all_objects = Debt.objects.filter(**filter_params)
        count_objects = all_objects.count()
        meta["resource_count"] = count_objects

        return all_objects.skip(offset).limit(page_size)


class DebtListCount(RetrieveAPI):
    serializer = DebtCountSerializer()

    error = BoolParam("Error filter")
    model = StringParam("Model filter")
    creator = StringParam("Creator filter")
    oracle = StringParam("Oracle filter")

    balance__lt = StringParam("Balance lt")
    balance__lte = StringParam("Balance lte")
    balance__gt = StringParam("Balance gt")
    balance__gte = StringParam("Balance gte")

    created__lt = StringParam("Created lt")
    created__lte = StringParam("Created lt")
    created__gt = StringParam("Created gt")
    created__gte = StringParam("Created gte")

    def retrieve(self, params, meta, **kwargs):
        # Filtering -> Ordering -> Limiting

        filter_params = params.copy()
        filter_params.pop("indent")

        all_objects = Debt.objects.filter(**filter_params)
        count_objects = all_objects.count()

        return {"count": count_objects}


class DebtItem(RetrieveAPI):
    serializer = DebtSerializer()

    def retrieve(self, params, meta, id_debt, **kwargs):
        try:
            return Debt.objects.get(id=id_debt)
        except Debt.DoesNotExist:
            raise falcon.HTTPNotFound(
                title='Debt does not exists',
                description='Debt with id={} does not exists'.format(id_debt)
            )


class ConfigList(PaginatedListAPI):
    serializer = ConfigSerializer()

    def list(self, params, meta, **kwargs):
        filter_params = params.copy()
        filter_params.pop("indent")

        page_size = filter_params.pop("page_size")
        page = filter_params.pop("page")

        offset = page * page_size

        all_objects = Config.objects.filter(**filter_params)
        count_objects = all_objects.count()
        meta["resource_count"] = count_objects

        return all_objects.skip(offset).limit(page_size)


class ConfigListCount(RetrieveAPI):
    serializer = ConfigCountSerializer()

    def retrieve(self, params, meta, **kwargs):
        filter_params = params.copy()
        filter_params.pop("indent")

        all_objects = Config.objects.filter(**filter_params)
        count_objects = all_objects.count()

        return {"count": count_objects}


class ConfigItem(RetrieveAPI):
    serializer = ConfigSerializer()

    def retrieve(self, params, meta, id_config, **kwargs):
        try:
            return Config.objects.get(id=id_config)
        except Config.DoesNotExist:
            raise falcon.HTTPNotFound(
                title='Config does not exists',
                description='Config with id={} does not exists'.format(id_config)
            )


class StateList(PaginatedListAPI):
    serializer = StateSerializer()

    status = StringParam("Status filter")

    def list(self, params, meta, **kwargs):
        filter_params = params.copy()
        filter_params.pop("indent")

        page_size = filter_params.pop("page_size")
        page = filter_params.pop("page")

        offset = page * page_size

        all_objects = State.objects.filter(**filter_params)
        count_objects = all_objects.count()
        meta["resource_count"] = count_objects

        return all_objects.skip(offset).limit(page_size)


class StateListCount(RetrieveAPI):
    serializer = StateCountSerializer()

    status = StringParam("Status filter")

    def retrieve(self, params, meta, **kwargs):
        filter_params = params.copy()
        filter_params.pop("indent")

        all_objects = State.objects.filter(**filter_params)
        count_objects = all_objects.count()

        return {"count": count_objects}


class StateItem(RetrieveAPI):
    serializer = StateSerializer()

    def retrieve(self, params, meta, id_state, **kwargs):
        try:
            return State.objects.get(id=id_state)
        except State.DoesNotExist:
            raise falcon.HTTPNotFound(
                title='State does not exists',
                description='State with id={} does not exists'.format(id_state)
            )


class LoanList(PaginatedListAPI):
    serializer = LoanSerializer()

    open = BoolParam("Open filter")
    approved = BoolParam("Approved filter")
    cosigner = StringParam("Cosigner filter")
    model = StringParam("Model filter")
    creator = StringParam("Creator filter")
    oracle = StringParam("Oracle filter")
    borrower = StringParam("Borrower filter")
    callback = StringParam("Callback filter")
    canceled = StringParam("Canceled filter")
    status = StringParam("Status Filter")
    lender = StringParam("Lender filter")

    expiration__lt = StringParam("Expiration lt")
    expiration__lte = StringParam("Expiration lte")
    expiration__gt = StringParam("Expiration gt")
    expiration__gte = StringParam("Expiration gte")

    amount__lt = StringParam("Amount lt")
    amount__lte = StringParam("Amount lte")
    amount__gt = StringParam("Amount gt")
    amount__gte = StringParam("Amount gte")

    created__lt = StringParam("Created lt")
    created__lte = StringParam("Created lte")
    created__gt = StringParam("Created gt")
    created__gte = StringParam("Created gte")


    def list(self, params, meta, **kwargs):
        # Filtering -> Ordering -> Limiting
        filter_params = params.copy()
        filter_params.pop("indent")

        page_size = filter_params.pop("page_size")
        page = filter_params.pop("page")

        offset = page * page_size

        all_objects = Loan.objects.filter(**filter_params)
        count_objects = all_objects.count()
        meta["resource_count"] = count_objects

        return all_objects.skip(offset).limit(page_size)


class LoanListCount(RetrieveAPI):
    serializer = LoanCountSerializer()

    open = BoolParam("Open filter")
    approved = BoolParam("Approved filter")
    cosigner = StringParam("Cosigner filter")
    model = StringParam("Model filter")
    creator = StringParam("Creator filter")
    oracle = StringParam("Oracle filter")
    borrower = StringParam("Borrower filter")
    callback = StringParam("Callback filter")
    canceled = StringParam("Canceled filter")
    status = StringParam("Status Filter")
    lender = StringParam("Lender filter")

    expiration__lt = StringParam("Expiration lt")
    expiration__lte = StringParam("Expiration lte")
    expiration__gt = StringParam("Expiration gt")
    expiration__gte = StringParam("Expiration gte")

    amount__lt = StringParam("Amount lt")
    amount__lte = StringParam("Amount lte")
    amount__gt = StringParam("Amount gt")
    amount__gte = StringParam("Amount gte")

    created__lt = StringParam("Created lt")
    created__lte = StringParam("Created lte")
    created__gt = StringParam("Created gt")
    created__gte = StringParam("Created gte")


    def retrieve(self, params, meta, **kwargs):
        # Filtering -> Ordering -> Limiting
        filter_params = params.copy()
        filter_params.pop("indent")

        all_objects = Loan.objects.filter(**filter_params)
        count_objects = all_objects.count()

        return {"count": count_objects}


class LoanItem(RetrieveAPI):
    serializer = LoanSerializer()

    def retrieve(self, params, meta, id_loan, **kwargs):
        try:
            return Loan.objects.get(id=id_loan)
        except Loan.DoesNotExist:
            raise falcon.HTTPNotFound(
                title="Loan does not exists",
                description="Loan with id={} does not exists".format(id_loan)
            )


class EntryList(PaginatedListAPI):
    serializer = EntrySerializer()

    def list(self, params, meta, **kwargs):
        # Filtering -> Ordering -> Limiting
        filter_params = params.copy()
        filter_params.pop("indent")

        page_size = filter_params.pop("page_size")
        page = filter_params.pop("page")

        offset = page * page_size

        all_objects = Entry.objects.filter(**filter_params)
        count_objects = all_objects.count()
        meta["resource_count"] = count_objects

        return all_objects.skip(offset).limit(page_size)


class EntryListCount(RetrieveAPI):
    serializer = EntryCountSerializer()

    def retrieve(self, params, meta, **kwargs):
        # Filtering -> Ordering -> Limiting
        filter_params = params.copy()
        filter_params.pop("indent")

        all_objects = Entry.objects.filter(**filter_params)
        count_objects = all_objects.count()

        return {"count": count_objects}


class EntryItem(RetrieveAPI):
    serializer = EntrySerializer()

    def retrieve(self, params, meta, id_entry, **kwargs):
        try:
            return Entry.objects.get(id=id_entry)
        except Entry.DoesNotExist:
            raise falcon.HTTPNotFound(
                title="Entry does not exists",
                description="Entry with id={} does not exists".format(id_entry)
            )


class CommitList(PaginatedListAPI):
    serializer = CommitSerializer()

    id_loan = StringParam("id_loan filter")
    opcode = StringParam("opcode filter")
    proof = StringParam("proof filter")
    address = StringParam("address filter")

    def list(self, params, meta, **kwargs):
        filter_params = params.copy()
        filter_params.pop("indent")

        page_size = filter_params.pop("page_size")
        page = filter_params.pop("page")

        offset = page * page_size

        all_objects = Commit.objects.filter(**filter_params)
        count_objects = all_objects.count()
        meta["resource_count"] = count_objects

        return all_objects.skip(offset).limit(page_size)


class CommitListCount(RetrieveAPI):
    serializer = CommitCountSerializer()

    def retrieve(self, params, meta, **kwargs):
        filter_params = params.copy()
        filter_params.pop("indent")

        all_objects = Commit.objects.filter(**filter_params)
        count_objects = all_objects.count()

        return {"count": count_objects}


class OracleHistoryList(PaginatedListAPI):
    serializer = OracleHistorySerializer()

    def list(self, params, meta, **kwargs):
        # Filtering -> Ordering -> Limiting
        filter_params = params.copy()
        filter_params.pop("indent")

        page_size = filter_params.pop("page_size")
        page = filter_params.pop("page")

        offset = page * page_size

        all_objects = OracleHistory.objects.filter(**filter_params)
        count_objects = all_objects.count()
        meta["resource_count"] = count_objects

        return all_objects.skip(offset).limit(page_size)


class OracleHistoryItem(RetrieveAPI):
    serializer = OracleHistorySerializer()

    def retrieve(self, params, meta, id_loan, **kwargs):
        try:
            return OracleHistory.objects.get(id=id_loan)
        except OracleHistory.DoesNotExist:
            raise falcon.HTTPNotFound(
                title="History does not exists",
                description="History with id={} does not exists".format(id_loan)
            )


class HealthStatusResource(object):
    def on_get(self, req, resp):
        clock = Clock()
        now = int(time.time())
        lower_limit = 60 * 2  # 2 minutes
        resp.status = falcon.HTTP_503
        is_sync = now - clock.time < lower_limit
        if is_sync:
            resp.status = falcon.HTTP_200


class ModelAndDebtDataResource(object):
    def on_get(self, req, resp, id_loan):
        try:
            data = get_data(id_loan)
            resp.body = json.dumps(data)
            resp.status = falcon.HTTP_200
        except Debt.DoesNotExist:
            raise falcon.HTTPNotFound(
                title="Debt does not exist",
                description="Debt with id={} does not exist".format(id_loan)
            )
        except Exception:
            raise falcon.HTTPNotFound(
                title="Error",
                description="An error ocurred :(".format(id_loan)
            )
