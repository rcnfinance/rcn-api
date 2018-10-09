from .commit_processor import CommitProcessor
from ..models import Loan

class LoanInDebtCommitProcessor(CommitProcessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opcode = "loan_in_debt"
        
    def process(self, commit, *args, **kwargs):
        data = commit.data
        opcode = commit.opcode
        
        loan = Loan.objects(index=data['loan']).first()
        assert loan.status == 1, "The loan was paid or destroyed"
        loan.commits.append(commit)
        loan.save()
        self.logger.info("Processing {} {} loan {}".format(commit.order, commit.opcode, loan.index))

        commit.loan = loan.to_dict()
        commit.save()