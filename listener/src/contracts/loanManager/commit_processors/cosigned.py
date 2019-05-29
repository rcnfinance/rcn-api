from models import Loan
from contracts.commit_processor import CommitProcessor


class Cosigned(CommitProcessor):
    def __init__(self):
        self.opcode = "cosigned_loan_manager"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        loan = Loan.objects.get(id=data.get("id"))

        loan.cosigner = data.get("cosigner")
        # loan.commits.append(commit)
        commit.save()
        loan.save()
