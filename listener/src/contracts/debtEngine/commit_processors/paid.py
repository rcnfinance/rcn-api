from models import Debt
from contracts.commit_processor import CommitProcessor


class Paid(CommitProcessor):
    def __init__(self):
        self.opcode = "paid_debt_engine"

    def process(self, commit, *args, **kwargs):
        data = commit.data
        debt = Debt.objects(id=data["id"]).first()

        new_balance = debt.balance + data.get("tokens")
        debt.balance = new_balance
        debt.commits.append(commit)

        debt.save()
