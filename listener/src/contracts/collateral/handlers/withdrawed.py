import web3
from contracts.event import EventHandler
from models import Commit


class Withdrawed(EventHandler):
    signature = "Withdrawed(uint256,address,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def handle(self):
        commit = Commit()

        commit.opcode = "withdrawed_collateral"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction
        commit.address = self._tx.get("from")

        data = {
            "id": str(self._args.get("_entryId")),
            "to": self._args.get("_to"),
            "amount": str(self._args.get("_amount"))
        }

        commit.data = data

        return [commit]
