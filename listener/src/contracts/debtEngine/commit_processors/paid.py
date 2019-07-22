from models import Debt
from contracts.commit_processor import CommitProcessor


class Paid(CommitProcessor):
    def __init__(self):
        super().__init__()
        self.opcode = "paid_debt_engine"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        try:
            debt = Debt.objects.get(id=data["id"])
            new_balance = int(debt.balance) + int(data.get("tokens"))
            debt.balance = str(new_balance)
            # debt.commits.append(commit)
            commit.save()
            debt.save()
        except Debt.DoesNotExist:
            self.logger.warning("Debt with id {} does not exist".format(data["id"]))
