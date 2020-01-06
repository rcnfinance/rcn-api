import web3
from contracts.event import EventHandler
from models import Commit


class Withdraw(EventHandler):
    signature = "Withdraw(uint256,address,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def handle(self):
        commit = Commit()

        commit.opcode = "withdraw_collateral"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction
        commit.address = self._tx.get("from")

        if str(self._args.get("_amount")) != '0':
            status = str(CollateralState.TO_WITHDRAW.value)

        data = {
            "id": str(self._args.get("_entryId")),
            "to": self._args.get("_to"),
            "amount": str(self._args.get("_amount")),
            "status": status
        }

        commit.data = data

        return [commit]
