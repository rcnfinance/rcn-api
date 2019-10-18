class SetURIProvider(CommitProcessor):
    def __init__(self):
        self.opcode = "set_max_spread_ratio"

    def process(self, commit, *args, **kwargs):
        #TODO
