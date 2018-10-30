import web3
from contracts.event import EventHandler


class Approval(EventHandler):
    signature = "Approval(address,address,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _parse(self):
        pass

    def handle(self):
        return []