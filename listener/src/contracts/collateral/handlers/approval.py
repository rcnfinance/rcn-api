import web3
from contracts.event import EventHandler
from models import Commit


class Approval(EventHandler):
    signature = "Approval(address,address,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def handle(self):
        commit = Commit()

        commit.opcode = "approval"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction

        data = {
            "owner": self._args.get("_owner"),
            "approved": self._args.get("_approved"),
            "tokenId": self._args.get("_tokenId")
        }

        commit.data = data

        return [commit]
