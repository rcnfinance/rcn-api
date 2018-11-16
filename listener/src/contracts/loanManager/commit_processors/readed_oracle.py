from contracts.commit_processor import CommitProcessor


class ReadedOracle(CommitProcessor):
    def __init__(self):
        self.opcode = "readed_oracle_loan_manager"

    def process(self, commit, *args, **kwargs):
        pass
