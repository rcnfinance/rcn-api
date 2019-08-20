from models import Debt
from contracts.commit_processor import CommitProcessor


class Error(CommitProcessor):
    def __init__(self):
        self.opcode = "error_debt_engine"

    def process(sielf, commit, *args, **kwargs):
        data = commit.new_data
        debt = Debt.objects(id=data["id"]).first()

        debt.error = data.get("error")

        old_data = {
            "id": data.get("id"),
            "error": debt.error
        }

        commit.old_data = old_data
        commit.save()
        debt.save()

    def apply_old(self, commit, *args, **kwargs):
        data = commit.old_data

        debt = Debt.objects.get(id=data.get("id"))

        debt.error = commit.data.get("error")

        debt.save()
        commit.delete()
