import falcon

from resources import LoanItem
from resources import LoanList
from resources import HealthStatusResource
from resources import CommitList
from falcon_cors import CORS
import db

cors = CORS(allow_all_origins=True)

api = application = falcon.API(middleware=[cors.middleware])

api.add_route("/v1/loans/", LoanList())
api.add_route("/v1/loans/{loan_index}/", LoanItem())
api.add_route("/v1/commits/", CommitList())
api.add_route("/health_status/", HealthStatusResource())