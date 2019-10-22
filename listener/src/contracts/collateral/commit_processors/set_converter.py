from contracts.commit_processor import CommitProcessor


class SetConverter(CommitProcessor):
    def __init__(self):
        self.opcode = "set_converter_collateral"

    def process(self, commit, *args, **kwargs):
        pass
