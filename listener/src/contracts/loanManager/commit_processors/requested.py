from models import Loan
from models import Descriptor
from contracts.commit_processor import CommitProcessor


class Requested(CommitProcessor):
    def __init__(self):
        self.opcode = "requested_loan_manager"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        loan = Loan()

        loan.id = data.get("id")
        loan.open = data.get("open")
        loan.approved = data.get("approved")
        loan.position = data.get("position")
        loan.expiration = data.get("expiration")
        loan.amount = data.get("amount")
        loan.cosigner = data.get("cosigner")
        loan.model = data.get("model")
        loan.creator = data.get("creator")
        loan.oracle = data.get("oracle")
        loan.borrower = data.get("borrower")
        loan.salt = data.get("salt")
        loan.loanData = data.get("loanData")
        loan.created = data.get("created")
        loan.descriptor = Descriptor(**data.get("descriptor"))
        loan.currency = data.get("currency")
        loan.status = data.get("status")
        # loan.commits.append(commit)
        commit.save()
        loan.save()
