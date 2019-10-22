from contracts.commit_processor import CommitProcessor


class PayOffDebt(CommitProcessor):
    def __init__(self):
        self.opcode = "pay_off_debt_collateral"

    def process(self, commit, *args, **kwargs):
        commit.save()
