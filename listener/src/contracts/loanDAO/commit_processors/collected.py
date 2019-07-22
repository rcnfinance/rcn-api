from models import Pool
from contracts.commit_processor import CommitProcessor


class Collected(CommitProcessor):
    def __init__(self):
        self.opcode = "collected_loanDAO"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        try:
            pool = Pool.objects.get(id=data["poolId"])
            new_collected = int(pool.collected) + int(data.get("amount"))
            pool.collected = str(new_collected)
            
            commit.save()
            pool.save()
        except Pool.DoesNotExist:
            self.logger.warning("Pool with id {} does not exist".format(data["poolId"]))