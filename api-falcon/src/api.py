import falcon

from resources import DebtItem
from resources import DebtList
from resources import ConfigItem
from resources import ConfigList
from resources import HealthStatusResource
from resources import LoanList
from resources import LoanItem
from resources import OracleHistoryList
from resources import OracleHistoryItem
from resources import ModelAndDebtDataResource
from falcon_cors import CORS
import db

cors = CORS(allow_all_origins=True)

api = application = falcon.API(middleware=[cors.middleware])

api.add_route("/health_status/", HealthStatusResource())

api.add_route("/v4/debts/", DebtList())
api.add_route("/v4/debts/{id_debt}/", DebtItem())

api.add_route("/v4/configs/", ConfigList())
api.add_route("/v4/configs/{id_config}/", ConfigItem())

api.add_route("/v4/loans/", LoanList())
api.add_route("/v4/loans/{id_loan}", LoanItem())

api.add_route("/v4/oracle_history/", OracleHistoryList())
api.add_route("/v4/oracle_history/{id_loan}", OracleHistoryItem())

api.add_route("/v4/model_debt_info/{id_loan}", ModelAndDebtDataResource())

