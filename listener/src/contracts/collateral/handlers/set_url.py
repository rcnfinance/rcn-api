import web3
from contracts.event import EventHandler
from models import Commit


class SetUrl(EventHandler):
    signature = "SetUrl(address)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def handle(self):
        commit = Commit()

        commit.opcode = "set_url_collateral"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction

        data = {
            "url": self._args.get("_url"),
        }

        commit.data = data

        return []
