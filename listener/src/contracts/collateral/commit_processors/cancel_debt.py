from models import Collateral
from contracts.commit_processor import CommitProcessor


class CancelDebt(CommitProcessor):
    def __init__(self):
        self.opcode = "cancel_debt_collateral"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        # TODO the loan its paid => status of the entry its payed
        # if ()
        #    collateral.status = CollateralState.PAYED.value

        commit.save()
        collateral.save()
