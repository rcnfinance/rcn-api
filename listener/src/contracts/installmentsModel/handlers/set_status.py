from contracts.event import EventHandler
import web3


class SetStatus(EventHandler):
    signature = "_setStatus(bytes32,uint8)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _parse(self):
        pass

    def handle(self):
        return []