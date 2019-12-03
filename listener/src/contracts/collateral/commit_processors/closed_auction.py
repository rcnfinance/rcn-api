from contracts.commit_processor import CommitProcessor


class ClosedAuction(CommitProcessor):
    def __init__(self):
        self.opcode = "closed_auction"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        collateral = Collateral.objects.get(id=data["id"])
        # TODO do something with "_received" argument
        # TODO do something with "_leftover" argument

        collateral.status = data.get("status")

        collateral.save()
        commit.save()
