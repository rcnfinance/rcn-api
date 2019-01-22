from models import Debt
from contracts.commit_processor import CommitProcessor


class Paid(CommitProcessor):
    def __init__(self):
        self.opcode = "paid_debt_engine"

    def process(self, commit, *args, **kwargs):
        data = commit.data
        debt = Debt.objects(id=data["id"]).first()

        new_balance = int(debt.balance) + int(data.get("tokens"))
        debt.balance = str(new_balance)
        debt.commits.append(commit)

        debt.save()
