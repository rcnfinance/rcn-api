from models import Debt
from contracts.commit_processor import CommitProcessor


class CreatedDebt(CommitProcessor):
    def __init__(self):
        self.opcode = "created_debt_engine"
        super().__init__()

    def process(self, commit, *args, **kwargs):
        data = commit.new_data
        debt = Debt()

        old_data = {
            "id": data.get("_id")
        }

        debt.id = data.get("id")
        debt.error = data.get("error")
        debt.balance = data.get("balance")
        debt.model = data.get("model")
        debt.creator = data.get("creator")
        debt.oracle = data.get("oracle")
        debt.created = data.get("created")

        commit.old_data = old_data
        commit.save()
        debt.save()

    def apply_old(self, commit, *args, **kwargs):
        data = commit.old_data

        debt = Debt.objects.get(id=data.get("id"))
        debt.delete()
        commit.delete()
