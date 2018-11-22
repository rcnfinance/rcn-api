from contracts.commit_processor import CommitProcessor


class ApprovedRejected(CommitProcessor):
    def __init__(self):
        self.opcode = "approved_rejected_loan_manager"

    def process(self, commit, *args, **kwargs):
        pass
