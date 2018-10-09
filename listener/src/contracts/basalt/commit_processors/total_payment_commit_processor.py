from .commit_processor import CommitProcessor
from ..models import Loan

class TotalPaymentCommitProcessor(CommitProcessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opcode = "total_payment"
        
    def process(self, commit, *args, **kwargs):
        data = commit.data
        opcode = commit.opcode
        
        loan = Loan.objects(index=data["loan"]).first()
        loan.status = 2
        loan.commits.append(commit)
        loan.save()
        self.logger.info("Processing {} {} loan {}".format(commit.order, commit.opcode, loan.index))

        commit.loan = loan.to_dict()
        commit.save()