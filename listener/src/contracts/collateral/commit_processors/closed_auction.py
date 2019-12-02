from contracts.commit_processor import CommitProcessor


class ClosedAuction(CommitProcessor):
    def __init__(self):
        self.opcode = "closed_auction"

    def process(self, commit, *args, **kwargs):
        # TODO implement
        pass
