from .commit_processor import CommitProcessor
from ..models import Loan

class PartialPaymentCommitProcessor(CommitProcessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opcode = "partial_payment"
        
    def process(self, commit, *args, **kwargs):
        data = commit.data
        opcode = commit.opcode
        
        loan = Loan.objects(index=data["loan"]).first()
        loan.paid = str(int(loan.paid) + int(data["amount"]))
        loan.commits.append(commit)

        loan.save()
        self.logger.info("Processing {} {} loan {}".format(commit.order, commit.opcode, loan.index))

        commit.loan = loan.to_dict()
        commit.save()