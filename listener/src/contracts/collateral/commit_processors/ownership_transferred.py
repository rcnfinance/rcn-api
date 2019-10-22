from contracts.commit_processor import CommitProcessor


class OwnershipTransferred(CommitProcessor):
    def __init__(self):
        self.opcode = "ownership_transferred_collateral"

    def process(self, commit, *args, **kwargs):
        pass
