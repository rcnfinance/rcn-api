from contracts.event import EventHandler
import web3


class ChangedDueTime(EventHandler):
    signature = "ChangedDueTime(bytes32,uint256,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _parse(self):
        pass

    def handle(self):
        return []
