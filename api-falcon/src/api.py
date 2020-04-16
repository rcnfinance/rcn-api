import falcon

from resources import DebtItem
from resources import DebtList
from resources import ConfigItem
from resources import ConfigList
from resources import HealthStatusResource
from resources import LoanList
from resources import LoanItem
from resources import StateList
from resources import StateItem
from resources import CommitList
from resources import CollateralList
from resources import CollateralItem
from resources import CompleteLoanList

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
api.add_route("/v4/loans/{id_loan}/", LoanItem())

api.add_route("/v4/states/", StateList())
api.add_route("/v4/states/{id_state}/", StateItem())

api.add_route("/v4/model_debt_info/{id_loan}/", ModelAndDebtDataResource())

api.add_route("/v4/commits/", CommitList())

api.add_route("/v4/collaterals/", CollateralList())
api.add_route("/v4/collaterals/{id_collateral}/", CollateralItem())

api.add_route("/v5/loans", CompleteLoanList())
