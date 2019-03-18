from models import Debt
from contracts.commit_processor import CommitProcessor


class Withdrawn(CommitProcessor):
    def __init__(self):
        self.opcode = "withdrawn_debt_engine"

    def process(self, commit, *args, **kwargs):
        data = commit.data
        print(data)
        debt = Debt.objects.get(id=data["id"])

        debt.balance = str(int(debt.balance) - int(data.get("amount")))

        debt.commits.append(commit)

        debt.save()
