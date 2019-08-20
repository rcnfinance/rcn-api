from models import Debt
from contracts.commit_processor import CommitProcessor


class ErrorRecover(CommitProcessor):
    def __init__(self):
        self.opcode = "error_recover_debt_engine"

    def process(self, commit, *args, **kwargs):
        data = commit.new_data
        debt = Debt.objects(id=data["id"]).first()

        old_data = {
            "id": Debt.objects(id=data.get("id")),
            "error": debt.error
        }
        debt.error = data.get("error")

        commit.old_data = old_data
        commit.save()
        debt.save()

    def apply_old(self, commit, *args, **kwargs):
        data = commit.old_data

        debt = Debt.objects(id=data["id"])
        debt.error = data.get("error")

        debt.save()
        commit.delete()
