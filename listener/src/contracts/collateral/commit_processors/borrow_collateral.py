from models import Collateral
from models import CollateralState
from contracts.commit_processor import CommitProcessor


class BorrowCollateral(CommitProcessor):
    def __init__(self):
        self.opcode = "borrow_collateral"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        collateral = Collateral.objects.get(id=data["id"])

        collateral.status = data.get("status")
        collateral.amount = data.get("newAmount")

        commit.save()
        collateral.save()
