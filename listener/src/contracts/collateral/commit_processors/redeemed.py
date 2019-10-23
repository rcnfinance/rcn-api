from models import Collateral
from models import CollateralState
from contracts.commit_processor import CommitProcessor


class Redeemed(CommitProcessor):
    def __init__(self):
        self.opcode = "redeemed_collateral"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        collateral = Collateral.objects.get(id=data["id"])
        collateral.status = CollateralState.CANCELED.value

        commit.save()
        collateral.save()
