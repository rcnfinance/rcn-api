from models import Debt
from contracts.commit_processor import CommitProcessor

class CreatedDebt(CommitProcessor):
    def __init__(self):
        self.opcode = "created_debt"

    def process(self, commit, *args, **kwargs):
        data = commit.data
        debt = Debt()
        print(data)
        debt.id = data.get("id")
        debt.error = data.get("error")
        debt.currency = data.get("currency")
        debt.balance = data.get("balance")
        debt.model = data.get("model")
        debt.creator = data.get("creator")
        debt.oracle = data.get("oracle")

        debt.save()