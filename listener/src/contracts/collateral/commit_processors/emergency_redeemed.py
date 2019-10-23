from models import Collateral
from contracts.commit_processor import CommitProcessor


class EmergencyRedeemed(CommitProcessor):
    def __init__(self):
        self.opcode = "emergency_redeemed_collateral"

    def process(self, commit, *args, **kwargs):
        pass
