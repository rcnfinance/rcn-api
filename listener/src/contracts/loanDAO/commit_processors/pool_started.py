from models import Pool
from contracts.commit_processor import CommitProcessor


class PoolStarted(CommitProcessor):
    def __init__(self):
        self.opcode = "pool_started_loanDAO"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        try:
            pool = Pool.objects.get(id=data["poolId"])
            pool.started = True
            
            commit.save()
            pool.save()
        except Pool.DoesNotExist:
            self.logger.warning("Pool with id {} does not exist".format(data["poolId"]))