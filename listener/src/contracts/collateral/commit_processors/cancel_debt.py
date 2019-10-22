from models import Collateral
from contracts.commit_processor import CommitProcessor


class CancelDebt(CommitProcessor):
    def __init__(self):
        self.opcode = "cancel_debt_collateral"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        entry = Collateral.objects.get(id=data.get("id"))

        entry.can_claim = data.get("can_claim")

        commit.save()
        entry.save()
