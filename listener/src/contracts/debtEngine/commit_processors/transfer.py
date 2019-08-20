from models import Loan
from contracts.commit_processor import CommitProcessor


class Transfer(CommitProcessor):
    def __init__(self):
        super().__init__()
        self.opcode = "transfer_debt_engine"

    def process(self, commit, *args, **kwargs):
        data = commit.new_data

        try:
            loan = Loan.objects.get(id=data.get("id"))

            old_data = {
                "id": data.get("id"),
                "lender": data.lender
            }

            loan.lender = data.get("to")
            commit.old_data = old_data
            commit.save()
            loan.save()
        except Loan.DoesNotExist:
            self.logger.warning("Loan with id {} does not exist".format(data["id"]))

    def apply_old(self, commit, *args, **kwargs):
        data = commit.old_data

        loan = Loan.objects.get(id=data.get("id"))

        loan.lender = data.get("lender")

        loan.save()
        commit.delete()
