from contracts.commit_processor import CommitProcessor
from models import State


class InstallmentsChangedStatus(CommitProcessor):
    def __init__(self):
        self.opcode = "changed_status_installments"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        try:
            state = State.object.get(id=data.get("id"))
        except State.DoesNotExist:
            state = State()
            state.id = data.get("id")

        state.status = data.get("status")
        state.commits.append(commit)

        state.save()
