import web3
from contracts.event import EventHandler


class SetEngine(EventHandler):
    signature = "_setEngine(address)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _parse(self):
        pass

    def handle(self):
        return []
