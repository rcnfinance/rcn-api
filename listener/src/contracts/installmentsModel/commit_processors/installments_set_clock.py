from contracts.commit_processor import CommitProcessor
from models import State


class InstallmentsSetClock(CommitProcessor):
    def __init__(self):
        self.opcode = "set_clock_installments"

    def process(self, commit, *args, **kwargs):
        data = commit.new_data

        try:
            state = State.objects.get(id=data.get("id"))
        except State.DoesNotExist:
            state = State()
            state.id = data.get("id")

        old_data = {
            "id": data.get("id"),
            "clock": state.clock
        }
        state.clock = data.get("duration")

        commit.old_data = old_data
        commit.save()
        state.save()

    def apply_old(self, commit, *args, **kwargs):
        data = commit.old_data

        state = State.objects.get(id=data.get("id"))

        state.clock = data.get("clock")

        state.save()
        commit.delete()
