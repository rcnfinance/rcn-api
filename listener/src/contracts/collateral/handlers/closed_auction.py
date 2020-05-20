import web3
from contracts.event import EventHandler
from models import Commit

from models import Loan
from models import Collateral
from models import CollateralState


class ClosedAuction(EventHandler):
    signature = "ClosedAuction(uint256,uint256,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def handle(self):
        commit = Commit()

        commit.opcode = "closed_auction"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction
        commit.address = self._tx.get("from")

        collateral_id = str(self._args.get("_entryId"))
        collateral = Collateral.objects.get(id=collateral_id)

        loan = Loan.objects.get(id=collateral.debt_id)
        if loan.status == "2":
            status = str(CollateralState.TO_WITHDRAW.value)
        else:
            status = str(CollateralState.STARTED.value)

        data = {
            "id": collateral_id,
            "received": str(self._args.get("_received")),
            "leftover": str(self._args.get("_leftover")),
            "status": status
        }

        commit.data = data

        return [commit]
