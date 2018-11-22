from models import Request
from contracts.commit_processor import CommitProcessor


class Canceled(CommitProcessor):
    def __init__(self):
        self.opcode = "canceled_loan_manager"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        request = Request.objects.get(id=data.get("id"))

        request.canceled = data.get("canceled")
        request.commits.append(commit)
        request.save()
