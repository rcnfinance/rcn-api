from models import Loan
from contracts.commit_processor import CommitProcessor


class Cosigned(CommitProcessor):
    def __init__(self):
        self.opcode = "cosigned_loan_manager"

    def process(self, commit, *args, **kwargs):
        data = commit.new_data

        loan = Loan.objects.get(id=data.get("id"))

        old_data = {
            "id": data.get("id"),
            "cosigner": loan.cosigner
        }

        loan.cosigner = data.get("cosigner")
        commit.old_data = old_data
        commit.save()
        loan.save()

    def apply_old(self, commit, *args, **kwargs):
        data = commit.old_data

        loan = Loan.objects.get(id=data.get("id"))

        loan.cosigner = data.get("cosigner")
        commit.delete()
        loan.save()
