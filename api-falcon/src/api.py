import falcon

from resources import DebtItem
from resources import DebtList
from resources import ConfigItem
from resources import ConfigList
from resources import HealthStatusResource
from resources import RequestList
from resources import RequestItem
from resources import OracleHistoryList
from resources import OracleHistoryItem
from falcon_cors import CORS
import db

cors = CORS(allow_all_origins=True)

api = application = falcon.API(middleware=[cors.middleware])

api.add_route("/health_status/", HealthStatusResource())

api.add_route("/v4/debts/", DebtList())
api.add_route("/v4/debts/{id_debt}/", DebtItem())

api.add_route("/v4/configs/", ConfigList())
api.add_route("/v4/configs/{id_config}/", ConfigItem())

api.add_route("/v4/requests", RequestList())
api.add_route("/v4/requests/{id_request}", RequestItem())

api.add_route("/v4/oracle_history/", OracleHistoryList())
api.add_route("/v4/oracle_history/{id_request}", OracleHistoryItem())
