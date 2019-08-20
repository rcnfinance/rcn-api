from models import Loan
from contracts.commit_processor import CommitProcessor


class Approved(CommitProcessor):
    def __init__(self):
        self.opcode = "approved_loan_manager"

    def process(self, commit, *args, **kwargs):
        data = commit.new_data

        loan = Loan.objects.get(id=data.get("id"))

        loan.approved = data.get("approved")
        commit.save()
        loan.save()

    def apply_old(self, commit, *args, **kwargs):
        data = commit.old_data
        loan = Loan.objects.get(id=data.get("id"))

        loan.approved = data.get("approved")
        commit.remove()
        loan.save()
