import web3
from contracts.event import EventHandler
from models import Commit


class Started(EventHandler):
    signature = "Started(uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def handle(self):
        commit = Commit()

        commit.opcode = "started_collateral"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction
        commit.address = self._tx.get("from")

        data = {
            "id": str(self._args.get("_entryId"))
        }

        commit.data = data

        return [commit]
