import web3
from contracts.event import EventHandler
import utils


class Transfer(EventHandler):
    signature = "Transfer(address,address,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _parse(self):
        # print(self._event)
        data = self._event.get("data")[2:]
        self._from = utils.to_address(web3.Web3.toHex(self._event.get("topics")[1]))
        self._to = utils.to_address(web3.Web3.toHex(self._event.get("topics")[2]))
        self._token_id = utils.to_int(data)

    def handle(self):
        return []
