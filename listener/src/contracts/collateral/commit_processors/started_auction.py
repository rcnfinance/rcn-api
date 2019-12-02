from contracts.commit_processor import CommitProcessor


class StartedAuction(CommitProcessor):
    def __init__(self):
        self.opcode = "started_auction"

    def process(self, commit, *args, **kwargs):
        # TODO implement
        pass
