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
from serializers import OracleHistorySerializer
from serializers import StateSerializer
from models import Debt
from models import Config
from models import Loan
from models import OracleHistory
from models import State
from clock import Clock
from utils import ModelAndDebtData

logger = logging.getLogger(__name__)

class DebtList(PaginatedListAPI):
    serializer = DebtSerializer()

    error = BoolParam("Error filter")
    model = StringParam("Model filter")
    creator = StringParam("Creator filter")
    oracle = StringParam("Oracle filter")

    def list(self, params, meta, **kwargs):
        # Filtering -> Ordering -> Limiting
        filter_params = params.copy()
        filter_params.pop("indent")

        page_size = filter_params.pop("page_size")
        page = filter_params.pop("page")

        offset = page * page_size

        return Debt.objects.filter(**filter_params).skip(offset).limit(page_size)


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

        return Config.objects.filter(**filter_params).skip(offset).limit(page_size)


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

        return State.objects.filter(**filter_params).skip(offset).limit(page_size)


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
    canceled = StringParam("Canceled filter")
    status = StringParam("Status Filter")

    def list(self, params, meta, **kwargs):
        # Filtering -> Ordering -> Limiting
        filter_params = params.copy()
        filter_params.pop("indent")

        page_size = filter_params.pop("page_size")
        page = filter_params.pop("page")

        offset = page * page_size

        return Loan.objects.filter(**filter_params).skip(offset).limit(page_size)


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


class OracleHistoryList(PaginatedListAPI):
    serializer = OracleHistorySerializer()

    def list(self, params, meta, **kwargs):
        # Filtering -> Ordering -> Limiting
        filter_params = params.copy()
        filter_params.pop("indent")

        page_size = filter_params.pop("page_size")
        page = filter_params.pop("page")

        offset = page * page_size

        return OracleHistory.objects.filter(**filter_params).skip(offset).limit(page_size)


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

        print(id_loan)
        modelAndDebtData = ModelAndDebtData()
        data = modelAndDebtData.getData(id_loan)
        
        print(data)    
        resp.body = json.dumps(data)
        resp.status = falcon.HTTP_200
