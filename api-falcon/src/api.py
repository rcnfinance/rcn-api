import falcon

from resources import DebtItem
from resources import DebtList
from resources import HealthStatusResource
from falcon_cors import CORS
import db

cors = CORS(allow_all_origins=True)

api = application = falcon.API(middleware=[cors.middleware])

# api.add_route("/v1/loans/", LoanList())
# api.add_route("/v1/loans/{loan_index}/", LoanItem())
api.add_route("/health_status/", HealthStatusResource())
api.add_route("/v4/debts/", DebtList())
api.add_route("/v4/debts/{id_loan}/", DebtItem())