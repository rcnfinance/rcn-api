from models import Request
from contracts.commit_processor import CommitProcessor


class Cosigned(CommitProcessor):
    def __init__(self):
        self.opcode = "cosigned_loan_manager"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        request = Request.objects.get(id=data.get("id"))

        request.cosigner = data.get("cosigner")
        request.commits.append(commit)
        request.save()
