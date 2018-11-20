import logging
import time
from graceful.resources.generic import RetrieveAPI
from graceful.resources.generic import PaginatedListCreateAPI
from graceful.parameters import StringParam
from graceful.parameters import BoolParam
import falcon
from serializers import DebtSerializer
from serializers import ConfigSerializer
from serializers import RequestSerializer
from serializers import OracleHistorySerializer
from models import Debt
from models import Config
from models import Request
from models import OracleHistory
from clock import Clock


logger = logging.getLogger(__name__)


class DebtList(PaginatedListCreateAPI):
    serializer = DebtSerializer()

    error = BoolParam("Error filter")
    currency = StringParam("Currency filter")
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
                description='Debt with index={} does not exists'.format(id_debt)
            )


class ConfigList(PaginatedListCreateAPI):
    serializer = ConfigSerializer()

    def list(self, params, meta, **kwargs):
        return Config.objects.all()


class ConfigItem(RetrieveAPI):
    serializer = ConfigSerializer()

    def retrieve(self, params, meta, id_config, **kwargs):
        try:
            return Config.objects.get(id=id_config)
        except Config.DoesNotExist:
            raise falcon.HTTPNotFound(
                title='Config does not exists',
                description='Config with index={} does not exists'.format(id_config)
            )


class RequestList(PaginatedListCreateAPI):
    serializer = RequestSerializer()

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

        return Request.objects.filter(**filter_params).skip(offset).limit(page_size)


class RequestItem(RetrieveAPI):
    serializer = RequestSerializer()

    def retrieve(self, params, meta, id_request, **kwargs):
        try:
            return Request.objects.get(id=id_request)
        except Request.DoesNotExist:
            raise falcon.HTTPNotFound(
                title="Request does not exists",
                description="Request with id={} does not exists".format(id_request)
            )


class OracleHistoryList(PaginatedListCreateAPI):
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

    def retrieve(self, params, meta, id_request, **kwargs):
        try:
            OracleHistory.objects.get(id=id_request)
        except OracleHistory.DoesNotExist:
            raise falcon.HTTPNotFound(
                title="History does not exists",
                description="History with id={} does not exists".format(id_request)
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
