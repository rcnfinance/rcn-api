from contracts.commit_processor import CommitProcessor


class InstallmentsAddedPaid(CommitProcessor):
    def __init__(self):
        self.opcode = " added_paid_installments"

    def process(self, commit, *args, **kwargs):
        pass
