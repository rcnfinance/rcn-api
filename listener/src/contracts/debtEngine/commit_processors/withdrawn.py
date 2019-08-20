from models import Debt
from contracts.commit_processor import CommitProcessor


class Withdrawn(CommitProcessor):
    def __init__(self):
        self.opcode = "withdrawn_debt_engine"

    def process(self, commit, *args, **kwargs):
        data = commit.new_data
        debt = Debt.objects.get(id=data["id"])

        old_data = {
            "id": data.get("id"),
            "balance": debt.balance
        }

        debt.balance = str(int(debt.balance) - int(data.get("amount")))

        commit.old_data = old_data
        commit.save()
        debt.save()

    def apply_old(self, commit, *args, **kwargs):
        data = commit.old_data

        debt = Debt.objects.get(id=data["id"])

        debt.balance = data.get("balance")

        debt.save()
        commit.delete()
