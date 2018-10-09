from .commit_processor import CommitProcessor
from ..models import Loan

class ApprovedLoanCommitProcessor(CommitProcessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opcode = "approved_loan"
    
    def process(self, commit, *args, **kwargs):
        data = commit.data
        opcode = commit.opcode
        
        loan = Loan.objects(index=data["loan"]).first()
        loan.approbations.append(data["approved_by"])
        loan.commits.append(commit)
        loan.save()
        self.logger.info("Processing {} {} loan {} by {}".format(commit.order, commit.opcode, loan.index, data['approved_by']))

        commit.loan = loan.to_dict()
        commit.save()