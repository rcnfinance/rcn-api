from .commit_processor import CommitProcessor
from ..models import Loan

class TransferCommitProcessor(CommitProcessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opcode = "transfer"
        
    def process(self, commit, *args, **kwargs):
        data = commit.data
        opcode = commit.opcode
        
        loan = Loan.objects(index=data['loan']).first()
        data['from'] = loan.lender
        loan.lender = data['to']
        loan.commits.append(commit)
        loan.save()
        self.logger.info("Processing {} {} loan {} from {} to {}".format(commit.order, commit.opcode, loan.index, data['from'], data['to']))

        commit.loan = loan.to_dict()
        commit.save()