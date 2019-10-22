from contracts.commit_processor import CommitProcessor


class Transfer(CommitProcessor):
    def __init__(self):
        self.opcode = "transfer"

    def process(self, commit, *args, **kwargs):
        pass
