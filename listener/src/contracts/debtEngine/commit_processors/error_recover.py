from models import Debt
from contracts.commit_processor import CommitProcessor


class ErrorRecover(CommitProcessor):
    def __init__(self):
        self.opcode = "error_recover_debt_engine"

    def process(self, commit, *args, **kwargs):
        data = commit.data
        debt = Debt.objects(id=data["id"]).first()

        debt.error = data.get("error")
        debt.commits.append(commit)
        debt.save()
