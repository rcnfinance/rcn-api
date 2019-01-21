from contracts.commit_processor import CommitProcessor
from models import State


class InstallmentsAddedPaid(CommitProcessor):
    def __init__(self):
        self.opcode = "added_paid_installments"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        try:
            state = State.objects.get(id=data.get("id"))
        except State.DoesNotExist:
            state = State()
            state.id = data.get("id")
        finally:
            state.last_payment = data.get("last_payment")
            state.paid = data.get("paid")
            state.commits.append(commit)

            state.save()
