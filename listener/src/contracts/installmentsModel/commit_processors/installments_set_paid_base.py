from contracts.commit_processor import CommitProcessor
from models import State


class InstallmentsSetPaidBase(CommitProcessor):
    def __init__(self):
        self.opcode = "set_paid_base_installments"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        try:
            state = State.objects.get(id=data.get("id"))
        except State.DoesNotExist:
            state = State()
            state.id = data.get("id")
        finally:
            state.paid_base = data.get("paid_base")
            state.commits.append(commit)

            state.save()
