import logging
import json
import falcon
from models import Debt
from utils import get_data


logger = logging.getLogger(__name__)


class ModelAndDebtDataResource(object):
    def on_get(self, req, resp, id_loan):
        try:
            data = get_data(id_loan)
            resp.body = json.dumps(data)
            resp.status = falcon.HTTP_200
        except Debt.DoesNotExist:
            raise falcon.HTTPNotFound(
                title="Debt does not exist",
                description="Debt with id={} does not exist".format(id_loan)
            )
        except Exception:
            raise falcon.HTTPNotFound(
                title="Error",
                description="An error ocurred :(".format(id_loan)
            )
