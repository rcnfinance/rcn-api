from models import Collateral
from models import CollateralState
from contracts.commit_processor import CommitProcessor


class Started(CommitProcessor):
    def __init__(self):
        self.opcode = "started_collateral"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        collateral = Collateral.objects.get(id=data["id"])
        collateral.status = CollateralState.STARTED.value

        for _collateral in Collateral.objects(debt_id=collateral.debt_id):
            _collateral.status = CollateralState.TO_REDEEM.value
            _collateral.save()

        commit.save()
        collateral.save()
