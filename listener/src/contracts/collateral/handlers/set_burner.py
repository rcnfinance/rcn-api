from contracts.event import EventHandler
import web3


class SetBurner(EventHandler):
    signature = "SetBurner(address)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def handle(self):
        return []
