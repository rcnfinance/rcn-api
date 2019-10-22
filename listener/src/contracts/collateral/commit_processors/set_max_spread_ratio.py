from contracts.commit_processor import CommitProcessor


class SetMaxSpreadRatio(CommitProcessor):
    def __init__(self):
        self.opcode = "set_max_spread_ratio"

    def process(self, commit, *args, **kwargs):
        pass
