from .commit_processor import CommitProcessor
from ..models import Loan

class InterestCommitProcessor(CommitProcessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opcode = "interest"
        
    def process(self, commit, *args, **kwargs):
        data = commit.data
        opcode = commit.opcode
        
        loan = Loan.objects(index=data['loan']).first()
        loan.interest_timestamp = data["interest_timestamp"]
        if "interest" in data:
            loan.interest = data["interest"]
            loan.punitory_interest = data["punitory_interest"]

        loan.commits.append(commit)
        loan.save()
        self.logger.info("Processing {} {} loan {}".format(commit.order, commit.opcode, loan.index))

        commit.loan = loan.to_dict()
        commit.save()