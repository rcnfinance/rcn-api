from .commit_processor import CommitProcessor
from ..models import Loan

class DestroyedLoanCommitProcessor(CommitProcessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opcode = "destroyed_loan"
    
    def process(self, commit, *args, **kwargs):
        data = commit.data
        opcode = commit.opcode
        
        loan = Loan.objects(index=data["loan"]).first()
        loan.status = 3
        loan.commits.append(commit)
        loan.save()
        self.logger.info("Processing {} {} loan {}".format(commit.order, commit.opcode, loan.index))

        commit.loan = loan.to_dict()
        commit.save()
