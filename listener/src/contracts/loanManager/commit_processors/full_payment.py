from models import Loan
from contracts.commit_processor import CommitProcessor


class FullPayment(CommitProcessor):
    def __init__(self):
        self.opcode = "full_payment_loan_manager"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        loan = Loan.objects.get(id=data.get("id"))

        loan.status = data.get("status")
        loan.commits.append(commit)
        loan.save()
