from contracts.commit_processor import CommitProcessor


class InstallmentsChangedStatus(CommitProcessor):
    def __init__(self):
        self.opcode = "changed_status_installments"

    def process(self, commit, *args, **kwargs):
        pass
