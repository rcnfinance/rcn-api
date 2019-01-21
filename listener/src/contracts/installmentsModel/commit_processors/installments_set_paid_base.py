from contracts.commit_processor import CommitProcessor
from models import State


class InstallmentsSetPaidBase(CommitProcessor):
    def __init__(self):
        self.opcode = "set_paid_base_installments"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        state = State.objects.get(id=data.get("id"))
        state.paid_base = data.get("paid_base")
        state.commits.append(commit)

        state.save()
