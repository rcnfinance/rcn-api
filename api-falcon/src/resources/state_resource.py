import logging
from graceful.resources.generic import RetrieveAPI
from graceful.resources.generic import PaginatedListAPI
from graceful.parameters import StringParam
import falcon
from serializers import StateSerializer
from models import State


logger = logging.getLogger(__name__)


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
