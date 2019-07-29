from models import Collateral
from contracts.commit_processor import CommitProcessor


class EmergencyRedeemed(CommitProcessor):
    def __init__(self):
        self.opcode = "emergency_redeemed_collateral"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        try:
            collateral = Collateral.objects.get(id=data["id"])
            collateral.amount = 0
            
            commit.save()
            collateral.save()
        except Collateral.DoesNotExist:
            self.logger.warning("Collateral with id {} does not exist".format(data["id"]))
