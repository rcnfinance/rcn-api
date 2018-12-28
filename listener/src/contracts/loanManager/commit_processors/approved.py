from models import Loan
from contracts.commit_processor import CommitProcessor


class Approved(CommitProcessor):
    def __init__(self):
        self.opcode = "approved_loan_manager"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        loan = Loan.objects.get(id=data.get("id"))

        loan.approved = data.get("approved")
        loan.commits.append(commit)
        loan.save()
