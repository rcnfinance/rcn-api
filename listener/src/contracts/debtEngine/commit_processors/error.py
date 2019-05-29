from models import Debt
from contracts.commit_processor import CommitProcessor


class Error(CommitProcessor):
    def __init__(self):
        self.opcode = "error_debt_engine"

    def process(sielf, commit, *args, **kwargs):
        data = commit.data
        debt = Debt.objects(id=data["id"]).first()

        debt.error = data.get("error")
        # debt.commits.append(commit)
        commit.save()
        debt.save()
