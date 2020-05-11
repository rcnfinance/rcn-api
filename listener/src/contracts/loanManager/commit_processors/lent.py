from models import Loan
from models import CollateralState
from models import Collateral
from contracts.commit_processor import CommitProcessor


class Lent(CommitProcessor):
    def __init__(self):
        self.opcode = "lent_loan_manager"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        loan = Loan.objects.get(id=data.get("id"))

        loan.open = data.get("open")
        loan.status = data.get("status")

        commit.save()
        loan.save()

        # To Collateral Cosigner Contract
        # for collateral in Collateral.objects(debt_id=data.get("id")):
        #     collateral.status = CollateralState.TO_REDEEM.value
        #     collateral.save()
