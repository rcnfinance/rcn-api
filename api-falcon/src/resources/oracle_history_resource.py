import logging
from graceful.resources.generic import RetrieveAPI
from graceful.resources.generic import PaginatedListAPI
import falcon
from serializers import OracleHistorySerializer
from models import OracleHistory


logger = logging.getLogger(__name__)


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
