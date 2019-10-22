from contracts.commit_processor import CommitProcessor


class CollateralBalance(CommitProcessor):
    def __init__(self):
        self.opcode = "collateral_balance_collateral"

    def process(self, commit, *args, **kwargs):
        commit.save()
