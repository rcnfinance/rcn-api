from models import Pool
from contracts.commit_processor import CommitProcessor


class PayBack(CommitProcessor):
    def __init__(self):
        self.opcode = "pay_back_loanDAO"

    def process(self, commit, *args, **kwargs):
        data = commit.data
        
        try:
            pool = Pool.objects.get(id=data["poolId"])
            
            commit.save()
            pool.save()
        except Pool.DoesNotExist:
            self.logger.warning("Pool with id {} does not exist".format(data["poolId"]))