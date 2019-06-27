from contracts.event import EventHandler
import web3


class Redeemed(EventHandler):
    signature = "Redeemed(uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def handle(self):
        return []
