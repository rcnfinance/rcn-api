from contracts.commit_processor import CommitProcessor


class TakeFee(CommitProcessor):
    def __init__(self):
        self.opcode = "take_fee_collateral"

    def process(self, commit, *args, **kwargs):
        commit.save()
