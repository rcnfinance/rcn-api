from contracts.commit_processor import CommitProcessor


class ApprovedError(CommitProcessor):
    def __init__(self):
        self.opcode = "approved_error_loan_manager"

    def process(self, commit, *args, **kwargs):
        pass

    def apply_old(self, commit, *args, **kwargs):
        commit.delete()
