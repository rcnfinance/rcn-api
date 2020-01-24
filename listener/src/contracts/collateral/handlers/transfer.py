import web3

from contracts.event import EventHandler
from models import Commit


class Transfer(EventHandler):
    signature = "Transfer(address,address,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def handle(self):
        commit = Commit()

        commit.opcode = "transfer_collateral"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction
        commit.address = self._tx.get("from")

        data = {
            "from": self._args.get("_from"),
            "to": self._args.get("_to"),
            "tokenId": str(self._args.get("_tokenId"))
        }

        commit.data = data

        return [commit]
