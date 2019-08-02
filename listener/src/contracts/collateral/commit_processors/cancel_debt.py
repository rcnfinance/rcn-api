from contracts.commit_processor import CommitProcessor

class CancelDebt(CommitProcessor):
    def __init__(self):
        self.opcode = "cancel_debt_collateral"

    def process(self, commit, *args, **kwargs):
        commit.save()

