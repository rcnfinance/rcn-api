from contracts.event import EventHandler
import web3


class SetUrl(EventHandler):
    signature = "SetUrl(string)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def handle(self):
        return []
