from models import Loan
from contracts.commit_processor import CommitProcessor


class Lent(CommitProcessor):
    def __init__(self):
        self.opcode = "lent_loan_manager"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        loan = Loan.objects.get(id=data.get("id"))

        loan.open = data.get("open")
        loan.lender = data.get("lender")
        loan.status = data.get("status")
        loan.commits.append(commit)

        loan.save()
