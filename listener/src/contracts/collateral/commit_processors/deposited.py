from models import Collateral
from contracts.commit_processor import CommitProcessor


class Deposited(CommitProcessor):
    def __init__(self):
        self.opcode = "deposited_collateral"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        collateral = Collateral.objects.get(id=data["id"])
        new_amount = collateral.amount + int(data.get("amount"))
        collateral.amount = str(new_amount)

        commit.save()
        collateral.save()