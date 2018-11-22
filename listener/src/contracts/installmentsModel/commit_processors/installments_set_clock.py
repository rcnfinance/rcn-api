from contracts.commit_processor import CommitProcessor


class InstallmentsSetClock(CommitProcessor):
    def __init__(self):
        self.opcode = "set_clock_installments"

    def process(self, commit, *args, **kwargs):
        pass
