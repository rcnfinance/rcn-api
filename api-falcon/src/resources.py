import datetime
import logging
import time
from graceful.resources.generic import RetrieveAPI
from graceful.resources.generic import PaginatedListCreateAPI
from graceful.parameters import StringParam
import falcon
from serializers import DebtSerializer
from models import Debt
from clock import Clock

logger = logging.getLogger(__name__)

class DebtList(PaginatedListCreateAPI):
    serializer = DebtSerializer()

    id = StringParam("id")
    error = StringParam("error")
    currency = StringParam("currency")
    balance = StringParam("balance")
    model = StringParam("model")
    creator = StringParam("creator")
    oracle = StringParam("oracle")

    def list(self, params, meta, **kwargs):
        return Debt.objects.all()

# class LoanList(PaginatedListCreateAPI):
#     serializer = LoanSerializer()
#     status = StringParam('Status filter')
#     creator = StringParam("Creator filter")
#     oracle = StringParam("Oracle filter")
#     borrower = StringParam("Borrower filter")
#     lender = StringParam("Borrower filter")
#     cosigner = StringParam("Cosigner filter")
#     approvedTransfer = StringParam("Approved Transfer filter")
#
#     def list(self, params, meta, **kwargs):
#         #  Filtering -> Ordering -> Limiting
#         filter_params = params.copy()
#         filter_params.pop("indent")
#         page_size = filter_params.pop("page_size")
#         page = filter_params.pop("page")
#         offset = (page) * page_size
#
#         return Loan.objects.filter(**filter_params).skip(offset).limit(page_size)


class DebtItem(RetrieveAPI):
    serializer = DebtSerializer()

    def retrieve(self, params, meta, id_debt, **kwargs):
        try:
            return Debt.objects.get(id=id_debt)
        except Debt.DoesNotExist:
            raise falcon.HTTPNotFound(
                title='Loan does not exists',
                description='Loan with index={} does not exists'.format(loan_index)
            )


# class LoanItem(RetrieveAPI):
#     serializer = LoanSerializer()
#
#     def retrieve(self, params, meta, loan_index, **kwargs):
#         try:
#             return Loan.objects.get(index=loan_index)
#         except Loan.DoesNotExist:
#             raise falcon.HTTPNotFound(
#                 title='Loan does not exists',
#                 description='Loan with index={} does not exists'.format(loan_index)
#             )


class HealthStatusResource(object):
    def on_get(self, req, resp):
        clock = Clock()
        now = int(time.time())
        lower_limit = 60 * 2 # 2 minutes
        resp.status = falcon.HTTP_503
        is_sync = now - clock.time < lower_limit
        print('Sync status {} progress {} current {}'.format(is_sync, clock.time, now))
        if is_sync:
            resp.status = falcon.HTTP_200
