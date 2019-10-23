from models import Collateral
from models import CollateralState
from models import Loan
from contracts.commit_processor import CommitProcessor


class CancelDebt(CommitProcessor):
    def __init__(self):
        self.opcode = "cancel_debt_collateral"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        collateral = Collateral.objects.get(id=data["id"])
        loan = Loan.objects.get(id=collateral.debt_id)

        if loan.status == "2":
            collateral.status = CollateralState.PAYED.value
            collateral.save()

        commit.save()
