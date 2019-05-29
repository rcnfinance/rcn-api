from contracts.event import EventHandler
import web3
import utils


class Created(EventHandler):
    signature = "Created(bytes32)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _normalize(self):
        self._args["_id"] = utils.add_0x_prefix(self._args["_id"].hex())

    def handle(self):
        return []
