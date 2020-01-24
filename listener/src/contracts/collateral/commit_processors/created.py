from models import Collateral
from contracts.commit_processor import CommitProcessor


class Created(CommitProcessor):
    def __init__(self):
        self.opcode = "created_collateral"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        collateral = Collateral.objects.get(id=data.get("id"))

        # Constants
        collateral.debt_id = data.get("debt_id")
        collateral.oracle = data.get("oracle")
        collateral.token = data.get("token")
        collateral.liquidation_ratio = data.get("liquidation_ratio")
        collateral.balance_ratio = data.get("balance_ratio")
        # Variable
        collateral.amount = data.get("amount")
        collateral.status = data.get("status")

        commit.save()
        collateral.save()
