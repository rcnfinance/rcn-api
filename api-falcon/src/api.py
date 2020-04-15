import falcon

from resources import DebtItem
from resources import DebtList
from resources import DebtListCount
from resources import ConfigItem
from resources import ConfigList
from resources import ConfigListCount
from resources import HealthStatusResource
from resources import LoanList
from resources import LoanItem
from resources import LoanListCount
from resources import OracleHistoryList
from resources import OracleHistoryItem
from resources import StateList
from resources import StateListCount
from resources import StateItem
from resources import CommitList
from resources import CommitListCount
from resources import CollateralList
from resources import CollateralListCount
from resources import CollateralItem
from resources import Coronavirus
from resources import CoronavirusList

from resources import ModelAndDebtDataResource
from falcon_cors import CORS
import db

cors = CORS(allow_all_origins=True)

api = application = falcon.API(middleware=[cors.middleware])

api.add_route("/health_status/", HealthStatusResource())

api.add_route("/v4/debts/", DebtList())
api.add_route("/v4/count/debts/", DebtListCount())
api.add_route("/v4/debts/{id_debt}/", DebtItem())

api.add_route("/v4/configs/", ConfigList())
api.add_route("/v4/count/configs/", ConfigListCount())
api.add_route("/v4/configs/{id_config}/", ConfigItem())

api.add_route("/v4/loans/", LoanList())
api.add_route("/v4/count/loans/", LoanListCount())
api.add_route("/v4/loans/{id_loan}/", LoanItem())

api.add_route("/v4/oracle_history/", OracleHistoryList())
api.add_route("/v4/oracle_history/{id_loan}", OracleHistoryItem())

api.add_route("/v4/states/", StateList())
api.add_route("/v4/count/states/", StateListCount())
api.add_route("/v4/states/{id_state}/", StateItem())

api.add_route("/v4/model_debt_info/{id_loan}/", ModelAndDebtDataResource())

api.add_route("/v4/commits/", CommitList())
api.add_route("/v4/count/commits/", CommitListCount())

api.add_route("/v4/collaterals/", CollateralList())
api.add_route("/v4/count/collaterals/", CollateralListCount())
api.add_route("/v4/collaterals/{id_collateral}/", CollateralItem())

api.add_route("/v5/covid/", Coronavirus())
api.add_route("/v5/covid2", CoronavirusList())
