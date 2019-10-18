import web3
from contracts.event import EventHandler
from models import Commit


class SetUrl(EventHandler):
    signature = "SetURIProvider(address)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def handle(self):
        commit = Commit()

        commit.opcode = "set_URIProvider_collateral"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction

        data = {
            "uriProvider": self._args.get("_uriProvider"),
        }

        commit.data = data

        return [commit]
