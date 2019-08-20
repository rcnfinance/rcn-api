from models import Loan
from contracts.commit_processor import CommitProcessor


class Lent(CommitProcessor):
    def __init__(self):
        self.opcode = "lent_loan_manager"

    def process(self, commit, *args, **kwargs):
        data = commit.new_data

        loan = Loan.objects.get(id=data.get("id"))

        old_data = {
            "id": data.get("id"),
            "lender": loan.lender,
            "open": loan.open,
            "status": loan.status
        }

        loan.open = data.get("open")
        loan.lender = data.get("lender")
        loan.status = data.get("status")

        commit.old_data = old_data
        commit.save()
        loan.save()

    def apply_old(self, commit, *args, **kwargs):
        data = commit.old_data

        loan = Loan.objects.get(id=data.get("id"))

        loan.open = data.get("open")
        loan.lender = data.get("lender")
        loan.status = data.get("status")

        loan.save()
        commit.delete()
