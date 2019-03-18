from models import Debt
from contracts.commit_processor import CommitProcessor


class CreatedDebt(CommitProcessor):
    def __init__(self):
        self.opcode = "created_debt_engine"

    def process(self, commit, *args, **kwargs):
        data = commit.data
        debt = Debt()
        debt.id = data.get("id")
        debt.error = data.get("error")
        debt.balance = data.get("balance")
        debt.model = data.get("model")
        debt.creator = data.get("creator")
        debt.oracle = data.get("oracle")
        debt.created = data.get("created")
        debt.commits.append(commit)

        print(debt.save())
