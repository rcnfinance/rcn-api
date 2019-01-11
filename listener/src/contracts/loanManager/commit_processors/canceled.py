from models import Loan
from contracts.commit_processor import CommitProcessor


class Canceled(CommitProcessor):
    def __init__(self):
        self.opcode = "canceled_loan_manager"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        loan = Loan.objects.get(id=data.get("id"))

        loan.canceled = data.get("canceled")
        loan.commits.append(commit)
        loan.save()
