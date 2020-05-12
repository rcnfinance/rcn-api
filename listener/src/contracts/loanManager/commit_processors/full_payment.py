from models import Loan
from models import Collateral
from models import CollateralState
from contracts.commit_processor import CommitProcessor


class FullPayment(CommitProcessor):
    def __init__(self):
        self.opcode = "full_payment_loan_manager"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        loan = Loan.objects.get(id=data.get("id"))

        loan.status = data.get("status")

        collaterals = Collateral.objects(debt_id=data.get("id"), status__in=["2", "3"])
        for collateral in collaterals:
            collateral.status = CollateralState.TO_WITHDRAW.value
            collateral.save()

        commit.save()
        loan.save()
