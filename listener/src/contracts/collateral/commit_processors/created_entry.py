from models import Entry
from contracts.commit_processor import CommitProcessor


class CreatedEntry(CommitProcessor):
    def __init__(self):
        self.opcode = "created_entry_collateral"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        entry = Entry()
        entry.id = data.get("id")
        entry.token = data.get("token")
        entry.debtId = data.get("debtId")
        entry.amount = data.get("amount")
        entry.liquidationRatio = data.get("liquidationRatio")
        entry.balanceRatio = data.get("balanceRatio")
        entry.burnFee = data.get("burnFee")
        entry.rewardFee = data.get("rewardFee")

        commit.save()
        entry.save()
