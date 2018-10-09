from .commit_processor import CommitProcessor
from ..models import Loan

class LoanExpiredCommitProcessor(CommitProcessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opcode = "loan_expired"
        
    def process(self, commit, *args, **kwargs):
        data = commit.data
        opcode = commit.opcode
        clock = kwargs.get("clock")
        
        loan = Loan.objects(index=data['loan']).first()
        assert loan.status == 0, "The loan was lent"
        assert int(loan.expiration_requests) <= clock, "The loan is not expired" # < or <= ? check contract
        loan.commits.append(commit)
        loan.save()
        self.logger.info("Processing {} {} loan {}".format(commit.order, commit.opcode, loan.index))
        commit.loan = loan.to_dict()
        commit.save()