from contracts.commit_processor import CommitProcessor
from models import State


class InstallmentsSetInterest(CommitProcessor):
    def __init__(self):
        self.opcode = "set_interest_installments"

    def process(self, commit, *args, **kwargs):
        data = commit.new_data

        try:
            state = State.objects.get(id=data.get("id"))
        except State.DoesNotExist:
            state = State()
            state.id = data.get("id")

        old_data = {
            "id": data.get("id"),
            "interest": state.interest
        }
        state.interest = data.get("interest")

        commit.old_data = old_data
        commit.save()
        state.save()

    def apply_old(self, commit, *args, **kwargs):
        data = commit.old_data

        state = State.objects.get(id=data.get("id"))

        state.interest = data.get("interest")

        state.save()
        commit.delete()
