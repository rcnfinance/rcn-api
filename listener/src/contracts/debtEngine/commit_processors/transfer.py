from models import Debt
from contracts.commit_processor import CommitProcessor


class Transfer(CommitProcessor):
    def __init__(self):
        super().__init__()
        self.opcode = "transfer_debt_engine"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        try:
            debt = Debt.objects.get(id=data.get("id"))
            debt.owner = data.get("to")

            commit.save()
            debt.save()
        except Debt.DoesNotExist:
            self.logger.warning("Debt with id {} does not exist".format(data["id"]))
