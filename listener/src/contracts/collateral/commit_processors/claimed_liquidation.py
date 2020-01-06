from contracts.commit_processor import CommitProcessor


class ClaimedLiquidation(CommitProcessor):
    def __init__(self):
        self.opcode = "claimed_liquidation_collateral"

    def process(self, commit, *args, **kwargs):
        # TODO implement
        pass
