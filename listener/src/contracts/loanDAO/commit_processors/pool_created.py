from models import Pool
from contracts.commit_processor import CommitProcessor


class PoolCreated(CommitProcessor):
    def __init__(self):
        self.opcode = "pool_created_loanDAO"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        pool = Pool()

        pool.id = data.get("poolId")
        pool.manager = data.get("manager")
        pool.loanId = data.get("loanId")
        pool.cosigner = data.get("cosigner")
        pool.cosigner_limit = data.get("cosignerLimit")
        pool.cosigner_data = data.get("cosignerData")
        pool.started = data.get("started")
        pool.tracker = data.get("tracker")
        pool.token = data.get("token")
        pool.raised = data.get("raised")
        pool.collected = data.get("collected")
        
        commit.save()
        pool.save()