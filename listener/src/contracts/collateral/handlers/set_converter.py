import web3
from contracts.event import EventHandler
from models import Commit


class SetConverter(EventHandler):
    signature = "SetConverter(address)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def handle(self):
        commit = Commit()

        commit.opcode = "set_converter_collateral"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction

        data = {
            "converter": self._args.get("_converter"),
        }

        commit.data = data

        return [commit]
