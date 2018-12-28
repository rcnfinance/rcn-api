from models import Request
from contracts.commit_processor import CommitProcessor


class Lent(CommitProcessor):
    def __init__(self):
        self.opcode = "lent_loan_manager"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        request = Request.objects.get(id=data.get("id"))

        request.open = data.get("open")
        request.commits.append(commit)

        request.save()
