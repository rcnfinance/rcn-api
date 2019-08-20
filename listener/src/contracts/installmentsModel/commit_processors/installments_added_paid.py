from contracts.commit_processor import CommitProcessor
from models import State


class InstallmentsAddedPaid(CommitProcessor):
    def __init__(self):
        self.opcode = "added_paid_installments"

    def process(self, commit, *args, **kwargs):
        data = commit.new_data

        try:
            state = State.objects.get(id=data.get("id"))
        except State.DoesNotExist:
            state = State()
            state.id = data.get("id")

        old_data = {
            "id": data.get("id"),
            "state_last_payment": data.get("state_last_payment"),
            "paid": data.get("paid")
        }

        state.last_payment = data.get("state_last_payment")
        state.paid = data.get("paid")

        commit.old_data = old_data
        commit.save()
        state.save()

    def apply_old(self, commit, *args, **kwargs):
        data = commit.old_data

        state = State.objects.get(id=data.get("id"))

        state.delete()
        commit.delete()
