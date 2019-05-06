from models import Loan
from contracts.commit_processor import CommitProcessor


class Transfer(CommitProcessor):
    def __init__(self):
        super().__init__()
        self.opcode = "transfer_debt_engine"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        try:
            loan = Loan.objects.get(id=data.get("id"))
            loan.lender = data.get("to")
            loan.commits.append(commit)
            loan.save()
        except Loan.DoesNotExist:
            self.logger.warning("Loan with id {} does not exist".format(data["id"]))
