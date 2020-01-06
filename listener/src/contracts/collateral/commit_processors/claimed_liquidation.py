from contracts.commit_processor import CommitProcessor


class ClaimedLiquidation(CommitProcessor):
    def __init__(self):
        self.opcode = "claimed_liquidation_collateral"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        collateral = Collateral.objects.get(id=data["id"])

        collateral.status = data.get("status")

        collateral.save()
        commit.save()
