import logging
import time
from graceful.resources.generic import RetrieveAPI
from graceful.resources.generic import PaginatedListCreateAPI
from graceful.parameters import StringParam
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

    def list(self, params, meta, **kwargs):
        return Debt.objects.all()


class DebtItem(RetrieveAPI):
    serializer = DebtSerializer()

    def retrieve(self, params, meta, id_debt, **kwargs):
        try:
            return Debt.objects.get(id=id_debt)
        except Debt.DoesNotExist:
            raise falcon.HTTPNotFound(
                title='Loan does not exists',
                description='Loan with index={} does not exists'.format(id_debt)
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

    def list(self, params, meta, **kwargs):
        return Request.objects.all()


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
        return OracleHistory.objects.all()


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
