from models import Request
from contracts.commit_processor import CommitProcessor


class Approved(CommitProcessor):
    def __init__(self):
        self.opcode = "approved_loan_manager"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        request = Request.objects.get(id=data.get("id"))

        request.approved = data.get("approved")
        request.commits.append(commit)
        request.save()
