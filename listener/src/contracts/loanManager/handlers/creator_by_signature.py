import web3
from contracts.event import EventHandler


class CreatorBySignature(EventHandler):
    signature = "CreatorBySignature(bytes32)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def handle(self):
        pass
