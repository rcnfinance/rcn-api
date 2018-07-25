import datetime
from graceful.resources.generic import RetrieveAPI
from graceful.resources.generic import PaginatedListCreateAPI
from graceful.parameters import StringParam
import falcon
from serializers import LoanSerializer
from models import Loan
from clock import Clock


class LoanList(PaginatedListCreateAPI):
    serializer = LoanSerializer()
    status = StringParam('Status filter')
    creator = StringParam("Creator filter")
    oracle = StringParam("Oracle filter")
    borrower = StringParam("Borrower filter")
    lender = StringParam("Borrower filter")
    cosigner = StringParam("Cosigner filter")
    approvedTransfer = StringParam("Approved Transfer filter")

    def list(self, params, meta, **kwargs):
        #  Filtering -> Ordering -> Limiting
        filter_params = params.copy()
        filter_params.pop("indent")
        page_size = filter_params.pop("page_size")
        page = filter_params.pop("page")
        offset = (page) * page_size

        return Loan.objects.filter(**filter_params).skip(offset).limit(page_size)



class LoanItem(RetrieveAPI):
    serializer = LoanSerializer()

    def retrieve(self, params, meta, loan_index, **kwargs):
        try:
            return Loan.objects.get(index=loan_index)
        except Loan.DoesNotExist:
            raise falcon.HTTPNotFound(
                title='Loan does not exists',
                description='Loan with index={} does not exists'.format(loan_index)
            )


class HealthStatusResource(object):
    def on_get(self, req, resp):
        clock = Clock()
        now = datetime.datetime.utcnow()
        lower_limit = datetime.timedelta(minutes=2)
        resp.status = falcon.HTTP_503
        is_sync = (now - lower_limit).timestamp() < clock.time
        if is_sync:
            resp.status = falcon.HTTP_200