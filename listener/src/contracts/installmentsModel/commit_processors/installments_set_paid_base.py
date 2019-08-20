from contracts.commit_processor import CommitProcessor
from models import State


class InstallmentsSetPaidBase(CommitProcessor):
    def __init__(self):
        self.opcode = "set_paid_base_installments"

    def process(self, commit, *args, **kwargs):
        data = commit.new_data

        state = State.objects.get(id=data.get("id"))

        old_data = {
            "id": data.get("id"),
            "paid_base": state.paid_base
        }
        state.paid_base = data.get("paid_base")

        commit.old_data = old_data
        commit.save()
        state.save()

    def apply_old(self, commit, *args, **kwargs):
        data = commit.old_data

        state = State.objects.get(id=data.get('id'))

        state.paid_base = data.get("paid_base")

        state.save()
        commit.delete()
