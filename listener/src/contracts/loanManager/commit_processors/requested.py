from models import Request
from contracts.commit_processor import CommitProcessor


class Requested(CommitProcessor):
    def __init__(self):
        self.opcode = "requested_loan_manager"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        request = Request()

        request.id = data.get("id")
        request.open = data.get("open")
        request.approved = data.get("approved")
        request.position = data.get("position")
        request.expiration = data.get("expiration")
        request.amount = data.get("amount")
        request.cosigner = data.get("cosigner")
        request.model = data.get("model")
        request.creator = data.get("creator")
        request.oracle = data.get("oracle")
        request.borrower = data.get("borrower")
        request.salt = data.get("salt")
        request.loanData = data.get("loanData")
        request.created = data.get("created")
        request.descriptor = data.get("descriptor")
        request.currency = data.get("currency")
        request.status = data.get("status")
        request.commits.append(commit)

        request.save()
