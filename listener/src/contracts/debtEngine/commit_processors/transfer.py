from models import Loan
from contracts.commit_processor import CommitProcessor


class Transfer(CommitProcessor):
    def __init__(self):
        super().__init__()
        self.opcode = "transfer_debt_engine"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        if data.from === "0x0":
            debt = Debt()
        else:
            debt = Debt.objects.get(id=data["id"])

        debt.owner = data.get("to")

        commit.save()
        debt.save()