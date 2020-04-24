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

        state.status = data.get("status")
        # state.commits.append(commit)
        commit.save()
        state.save()

        # To Collateral Cosigner Contract
        collateral = Collateral.objects.get(debt_id=data.get("id"))
        collateral.status = CollateralState.TO_WITHDRAW.value
        collateral.save()