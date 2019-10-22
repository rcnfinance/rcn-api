from models import Collateral
from contracts.commit_processor import CommitProcessor


class Started(CommitProcessor):
    def __init__(self):
        self.opcode = "started_collateral"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        try:
            collateral = Collateral.objects.get(id=data["id"])
            collateral.started = True

            commit.save()
            collateral.save()
        except Collateral.DoesNotExist:
            self.logger.warning("Collateral with id {} does not exist".format(data["id"]))
