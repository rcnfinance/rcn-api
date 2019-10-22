from contracts.commit_processor import CommitProcessor


class SetUrl(CommitProcessor):
    def __init__(self):
        self.opcode = "set_url_collateral"

    def process(self, commit, *args, **kwargs):
        pass
