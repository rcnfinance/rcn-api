import falcon

from resources import LoanItem
from resources import LoanList
import db

api = application = falcon.API()

api.add_route("/v1/loans/", LoanList())
api.add_route("/v1/loans/{loan_index}/", LoanItem())
