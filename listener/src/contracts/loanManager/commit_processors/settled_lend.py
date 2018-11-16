from contracts.commit_processor import CommitProcessor


class SettledLend(CommitProcessor):
    def __init__(self):
        self.opcode = "settled_lend_loan_manager"

    def process(self, commit, *args, **kwargs):
        pass
