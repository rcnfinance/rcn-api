import web3
from contracts.event import EventHandler
from models import Commit


class ApprovalForAll(EventHandler):
    signature = "ApprovalForAll(address,address,bool)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def handle(self):
        commit = Commit()

        commit.opcode = "approval_for_all"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction

        data = {
            "owner": self._args.get("_owner"),
            "operator": self._args.get("_operator"),
            "approved": self._args.get("_approved")
        }

        commit.data = data

        return [commit]
