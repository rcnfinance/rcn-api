from models import Pool
from contracts.commit_processor import CommitProcessor


class Join(CommitProcessor):
    def __init__(self):
        self.opcode = "join_loanDAO"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        try:
            pool = Pool.objects.get(id=data["poolId"])
            new_raised = int(pool.raised) + int(data.get("tokens"))
            pool.raised = str(new_raised)
            
            commit.save()
            pool.save()
        except Pool.DoesNotExist:
            self.logger.warning("Pool with id {} does not exist".format(data["poolId"]))