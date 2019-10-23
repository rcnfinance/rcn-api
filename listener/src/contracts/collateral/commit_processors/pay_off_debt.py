from models import Collateral
from models import CollateralState
from contracts.commit_processor import CommitProcessor

class PayOffDebt(CommitProcessor):
    def __init__(self):
        self.opcode = "pay_off_debt_collateral"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        # if (int(data.get("payTokens") >= int(data.get("closingObligationToken"))
        #     collateral = Collateral.objects.get(id=data["id"])
        #     collateral.status = CollateralState.PAYED.value
        #     collateral.save()

        commit.save()
