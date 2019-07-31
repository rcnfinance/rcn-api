from models import Collateral
from contracts.commit_processor import CommitProcessor


class TakeFee(CommitProcessor):
    def __init__(self):
        self.opcode = "take_fee_collateral"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        try:
            collateral = Collateral.objects.get(id=data["id"])
            new_amount = int(collateral.amount) - int(data.get("burned")) - int(data.get("rewarded"))
            collateral.amount = str(new_amount)
            
            commit.save()
            collateral.save()
        except Collateral.DoesNotExist:
            self.logger.warning("Collateral with id {} does not exist".format(data["id"]))