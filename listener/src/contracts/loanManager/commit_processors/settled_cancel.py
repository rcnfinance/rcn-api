from contracts.commit_processor import CommitProcessor


class SettledCancel(CommitProcessor):
    def __init__(self):
        self.opcode = "settled_cancel_loan_manager"

    def process(self, commit, *args, **kwargs):
        pass
