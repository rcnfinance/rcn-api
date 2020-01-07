from models import Collateral
from contracts.commit_processor import CommitProcessor


class Redeemed(CommitProcessor):
    def __init__(self):
        self.opcode = "redeemed_collateral"

    def process(self, commit, *args, **kwargs):
        pass
