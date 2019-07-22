import web3
from contracts.event import EventHandler


class SetDescriptor(EventHandler):
    signature = "_setDescriptor(address)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def handle(self):
        return []
