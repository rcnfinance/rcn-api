from contracts.event import EventHandler
import web3


class SetClock(EventHandler):
    signature = "_setClock(bytes32,uint64)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _parse(self):
        pass

    def handle(self):
        return []