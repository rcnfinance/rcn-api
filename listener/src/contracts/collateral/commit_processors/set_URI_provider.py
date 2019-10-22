from contracts.commit_processor import CommitProcessor


class SetURIProvider(CommitProcessor):
    def __init__(self):
        self.opcode = "set_URIProvider_collateral"

    def process(self, commit, *args, **kwargs):
        pass
