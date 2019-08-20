from models import Loan
from contracts.commit_processor import CommitProcessor


class Canceled(CommitProcessor):
    def __init__(self):
        self.opcode = "canceled_loan_manager"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        loan = Loan.objects.get(id=data.get("id"))

        old_data = {
            "id": commit.new_data.get("id"),
            "canceled": loan.canceled
        }

        loan.canceled = data.get("canceled")

        commit.old_data = old_data
        commit.save()
        loan.save()

    def apply_old(self, commit, *args, **kwargs):
        old_data = commit.old_data

        loan = Loan.objects.get(id=self._args.get("_id"))
        loan.canceled = old_data.get("canceled")
        loan.save()
        commit.delete()
