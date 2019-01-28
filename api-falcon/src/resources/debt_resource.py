import logging
from graceful.resources.generic import RetrieveAPI
from graceful.resources.generic import PaginatedListAPI
from graceful.parameters import StringParam
from graceful.parameters import BoolParam
import falcon
from serializers import DebtSerializer

from models import Debt

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
