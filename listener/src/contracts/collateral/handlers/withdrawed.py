from contracts.event import EventHandler
import web3


class Withdrawed(EventHandler):
    signature = "Withdrawed(uint256,address,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def handle(self):
        return []
