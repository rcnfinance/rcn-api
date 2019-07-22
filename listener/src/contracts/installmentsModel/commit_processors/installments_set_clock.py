from contracts.commit_processor import CommitProcessor
from models import State


class InstallmentsSetClock(CommitProcessor):
    def __init__(self):
        self.opcode = "set_clock_installments"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        try:
            state = State.objects.get(id=data.get("id"))
        except State.DoesNotExist:
            state = State()
            state.id = data.get("id")

        state.clock = data.get("duration")
        # state.commits.append(commit)
        commit.save()
        state.save()
