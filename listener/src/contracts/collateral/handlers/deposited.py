import web3
from contracts.event import EventHandler
from models import Commit

from models import Collateral
from models import CollateralState


class Deposited(EventHandler):
    signature = "Deposited(uint256,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def handle(self):
        commit = Commit()

        commit.opcode = "deposited_collateral"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction
        commit.address = self._tx.get("from")

        id = str(self._args.get("_entryId"))
        amount = str(self._args.get("_amount"))
        collateral = Collateral.objects.get(id=id)
        if collateral.status == CollateralState.FINISH.value and amount != '0':
            status = str(CollateralState.TO_WITHDRAW.value)
        else:
            status = str(collateral.status)

        data = {
            "id": id,
            "amount": amount,
            "status": status
        }

        commit.data = data

        return [commit]
