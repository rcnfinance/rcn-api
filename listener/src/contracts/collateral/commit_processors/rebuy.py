from contracts.commit_processor import CommitProcessor


class Rebuy(CommitProcessor):
    def __init__(self):
        self.opcode = "rebuy_collateral"

    def process(self, commit, *args, **kwargs):
        pass
