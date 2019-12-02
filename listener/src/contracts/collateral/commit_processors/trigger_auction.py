from contracts.commit_processor import CommitProcessor


class TriggerAuction(CommitProcessor):
    def __init__(self):
        self.opcode = "trigger_auction"

    def process(self, commit, *args, **kwargs):
        # TODO implement
        pass
