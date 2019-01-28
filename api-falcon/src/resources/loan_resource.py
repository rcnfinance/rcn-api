import logging
from graceful.resources.generic import RetrieveAPI
from graceful.resources.generic import PaginatedListAPI
from graceful.parameters import StringParam
from graceful.parameters import BoolParam
import falcon
from serializers import LoanSerializer
from models import Loan


logger = logging.getLogger(__name__)


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
