import logging
from graceful.resources.generic import RetrieveAPI
from graceful.resources.generic import PaginatedListAPI
import falcon
from serializers import ConfigSerializer
from models import Config


logger = logging.getLogger(__name__)


class ConfigList(PaginatedListAPI):
    serializer = ConfigSerializer()

    def list(self, params, meta, **kwargs):
        filter_params = params.copy()
        filter_params.pop("indent")

        page_size = filter_params.pop("page_size")
        page = filter_params.pop("page")

        offset = page * page_size

        all_objects = Config.objects.filter(**filter_params)
        count_objects = all_objects.count()
        meta["resource_count"] = count_objects

        return all_objects.skip(offset).limit(page_size)


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
