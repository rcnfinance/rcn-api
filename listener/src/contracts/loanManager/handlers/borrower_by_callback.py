import web3
from contracts.event import EventHandler


class BorrowerByCallback(EventHandler):
    signature = "BorrowerByCallback(bytes32)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _parse(self):
        pass

    def handle(self):
        pass
