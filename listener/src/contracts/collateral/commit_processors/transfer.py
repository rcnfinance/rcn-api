from models import Collateral
from contracts.commit_processor import CommitProcessor


class Transfer(CommitProcessor):
    def __init__(self):
        self.opcode = "transfer_collateral"

    def process(self, commit, *args, **kwargs):
        data = commit.data
        print(data.get("tokenId"))

        collateral = Collateral()

        collateral.id = data.get("tokenId")
        collateral.owner = data.get("to")

        commit.save()
        collateral.save()
