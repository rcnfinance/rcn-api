from contracts.commit_processor import CommitProcessor


class ApprovalForAll(CommitProcessor):
    def __init__(self):
        self.opcode = "approval_for_all_collateral"

    def process(self, commit, *args, **kwargs):
        pass
