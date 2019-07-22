import logging
import time
import falcon

from graceful.resources.generic import RetrieveAPI, PaginatedListAPI
from graceful.parameters import StringParam

from serializers import LoanSerializer
from serializers import CommitSerializer
from models import Loan
from models import Commit
from clock import Clock

logger = logging.getLogger(__name__)


class LoanList(PaginatedListAPI):
    serializer = LoanSerializer()
    status = StringParam('Status filter')
    creator = StringParam("Creator filter")
    oracle = StringParam("Oracle filter")
    borrower = StringParam("Borrower filter")
    lender = StringParam("Borrower filter")
    cosigner = StringParam("Cosigner filter")
    approvedTransfer = StringParam("Approved Transfer filter")

    created__lt = StringParam("Created lt")
    created__lte = StringParam("Created lte")
    created__gt = StringParam("Created gt")
    created__gte = StringParam("Created gte")

    amount__lt = StringParam("Amount lt")
    amount__lte = StringParam("Amount lte")
    amount__gt = StringParam("Amount gt")
    amount__gte = StringParam("Amount gte")

    interest__lt = StringParam("Interest lt")
    interest__lte = StringParam("Interest lte")
    interest__gt = StringParam("Interest gt")
    interest__gte = StringParam("Interest gte")

    punitory_interest__lt = StringParam("Punitory interest lt")
    punitory_interest__lte = StringParam("Punitory interest lte")
    punitory_interest__gt = StringParam("Punitory interest gt")
    punitory_interest__gte = StringParam("Punitory interest gte")

    interest_timestamp__lt = StringParam("Interest timestamp lt")
    interest_timestamp__lte = StringParam("Interest timestamp lte")
    interest_timestamp__gt = StringParam("Interest timestamp gt")
    interest_timestamp__gte = StringParam("Interest timestamp gte")

    paid__lt = StringParam("Paid lt")
    paid__lte = StringParam("Paid lte")
    paid__gt = StringParam("Paid gt")
    paid__lte = StringParam("Paid gte")

    interest_rate__lt = StringParam("Interest rate lt")
    interest_rate__lte = StringParam("Interest rate lte")
    interest_rate__gt = StringParam("Interest rate gt")
    interest_rate__gte = StringParam("Interest rate gte")

    interest_rate_punitory__lt = StringParam("Interest rate punitory lt")
    interest_rate_punitory__lte = StringParam("Interest rate punitory lte")
    interest_rate_punitory__gt = StringParam("Interest rate punitory gt")
    interest_rate_punitory__gte = StringParam("Interest rate punitory gte")

    due_time__lt = StringParam("Due time lt")
    due_time__lte = StringParam("Due time lte")
    due_time__gt = StringParam("Due time gt")
    due_time__gte = StringParam("Due time gte")

    dues_in__lt = StringParam("Dues in lt")
    dues_in__lte = StringParam("Dues in lte")
    dues_in__gt = StringParam("Dues in gt")
    dues_in__gte = StringParam("Dues in gte")

    cancelable_at__lt = StringParam("Cancelable at lt")
    cancelable_at__lte = StringParam("Cancelable at lte")
    cancelable_at__gt = StringParam("Cancelable at gt")
    cancelable_at__gte = StringParam("Cancelable at gte")

    lender_balance__lt = StringParam("Lender balance lt")
    lender_balance__lte = StringParam("Lender balance lte")
    lender_balance__gt = StringParam("Lender balance gt")
    lender_balance__gte = StringParam("Lender balance gte")

    expiration_requests__lt = StringParam("Expiration request lt")
    expiration_requests__lte = StringParam("Expiration request lte")
    expiration_requests__gt = StringParam("Expiration request gt")
    expiration_requests__gte = StringParam("Expiration request gte")

    def list(self, params, meta, **kwargs):
        #  Filtering -> Ordering -> Limiting
        filter_params = params.copy()
        filter_params.pop("indent")
        page_size = filter_params.pop("page_size")
        page = filter_params.pop("page")
        offset = page * page_size

        return Loan.objects.filter(**filter_params).skip(offset).limit(page_size)


class CommitList(PaginatedListAPI):
    serializer = CommitSerializer()

    id_loan = StringParam("id_loan filter")
    opcode = StringParam("opcode filter")
    proof = StringParam("proof filter")

    timestamp__lt = StringParam("Timestamp lt")
    timestamp__lte = StringParam("Timestamp lte")
    timestamp__gt = StringParam("Timestamp gt")
    timestamp__gte = StringParam("Timestamp gte")

    def list(self, params, meta, **kwargs):
        filter_params = params.copy()
        filter_params.pop("indent")

        page_size = filter_params.pop("page_size")
        page = filter_params.pop("page")

        offset = page * page_size

        return Commit.objects.filter(**filter_params).skip(offset).limit(page_size)


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
        now = int(time.time())
        lower_limit = 60 * 2  # 2 minutes
        resp.status = falcon.HTTP_503
        is_sync = now - clock.time < lower_limit
        print('Sync status {} progress {} current {}'.format(is_sync, clock.time, now))
        if is_sync:
            resp.status = falcon.HTTP_200
