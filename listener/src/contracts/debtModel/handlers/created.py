from contracts.event import EventHandler
import web3


class Created(EventHandler):
    signature = "Created(bytes32)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _parse(self):
        print(self._event.get("topics"))
        self._id = self._event.get("topics")[1].hex()
        self._block_number = self._event.get('blockNumber')
        self._transaction = self._event.get('transactionHash').hex()

    def handle(self):
        return []
