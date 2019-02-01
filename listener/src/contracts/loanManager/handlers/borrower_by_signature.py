import web3
from contracts.event import EventHandler


class BorrowerBySignature(EventHandler):
    signature = "BorrowerBySignature(bytes32)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def handle(self):
        pass
