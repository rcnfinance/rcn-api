from contracts.event import EventHandler
import web3


class ChangedFinalTime(EventHandler):
    signature = "ChangedFinalTime(bytes32,uint256,uint64)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _parse(self):
        pass

    def handle(self):
        return []
