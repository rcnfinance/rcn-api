import web3
from contracts.event import EventHandler


class ReadedOracleBatch(EventHandler):
    signature = "ReadedOracleBatch(address,uint256,uint256,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _parse(self):
        self._data = self._event.get("data")
        self._id = self._event.get("topics")[1].hex()
        self._block_number = self._event.get('blockNumber')
        self._transaction = self._event.get('transactionHash').hex()

    def handle(self):
        return []
