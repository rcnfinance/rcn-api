from models import Collateral
from contracts.commit_processor import CommitProcessor


class CollateralBalance(CommitProcessor):
    def __init__(self):
        self.opcode = "collateral_balance_collateral"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        try:
            collateral = Collateral.objects.get(id=data["id"])
            new_amount = int(collateral.amount) - int(data.get("payTokens"))
            collateral.amount = str(new_amount)
            
            commit.save()
            collateral.save()
        except Collateral.DoesNotExist:
            self.logger.warning("Collateral with id {} does not exist".format(data["id"]))
