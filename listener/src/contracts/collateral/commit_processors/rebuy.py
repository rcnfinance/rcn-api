from models import Collateral
from contracts.commit_processor import CommitProcessor


class Rebuy(CommitProcessor):
    def __init__(self):
        self.opcode = "rebuy_collateral"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        collateral = Collateral.objects.get(id=data["id"])
        new_amount = int(collateral.amount) + int(data.get("toAmount"))
        collateral.amount = str(new_amount)

        commit.save()
        collateral.save()
