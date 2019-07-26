from models import Collateral, Loan
from contracts.commit_processor import CommitProcessor


class Created(CommitProcessor):
    def __init__(self):
        self.opcode = "created_collateral"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        loan = Loan.objects.get(id=data.get("debt_id"))

        collateral = Collateral()

        collateral.id = data.get("id")
        collateral.debt_id = data.get("debt_id")
        collateral.token = data.get("token")
        collateral.amount = data.get("amount")
        collateral.liquidation_ratio = data.get("liquidation_ratio")
        collateral.balance_ratio = data.get("balance_ratio")
        collateral.burn_fee = data.get("burn_fee")
        collateral.reward_fee = data.get("reward_fee")
 
        loan.collaterals.append(collateral)
        commit.save()
        collateral.save()
