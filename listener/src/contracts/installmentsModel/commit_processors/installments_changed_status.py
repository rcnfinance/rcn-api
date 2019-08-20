from contracts.commit_processor import CommitProcessor
from models import State


class InstallmentsChangedStatus(CommitProcessor):
    def __init__(self):
        self.opcode = "changed_status_installments"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        try:
            state = State.objects.get(id=data.get("id"))
        except State.DoesNotExist:
            state = State()
            state.id = data.get("id")

        old_data = {
            "id": data.get("id"),
            "status": state.status
        }

        state.status = data.get("status")

        commit.old_data = old_data
        commit.save()
        state.save()

    def apply_old(self, commit, *args, **kwargs):
        data = commit.old_data

        state = State.objects.get(id=data.get("id"))

        state.status = data.get("status")

        state.save()
        commit.delete()
