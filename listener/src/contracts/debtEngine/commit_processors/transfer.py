from models import Loan
from contracts.commit_processor import CommitProcessor


class Transfer(CommitProcessor):
    def __init__(self):
        self.opcode = "transfer_debt_engine"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        loan = Loan.objects.get(id=data.get("id"))
        loan.lender = data.get("to")
        loan.commits.append(commit)
        loan.save()
