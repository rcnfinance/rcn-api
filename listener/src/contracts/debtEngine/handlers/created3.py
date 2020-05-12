import web3
from contracts.event import EventHandler
from models import Commit
from contracts.debtEngine.debt_engine import debt_engine_interface


class Created3(EventHandler):
    signature = "Created3(bytes32,uint256,bytes)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _normalize(self):
        self._args["_id"] = utils.add_0x_prefix(self._args["_id"].hex())

    def handle(self):
        return []
