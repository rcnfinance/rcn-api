from contracts.event import EventHandler
import web3
import utils


class AddedPaid(EventHandler):
    signature = "AddedPaid(bytes32,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _normalize(self):
        self._args["_id"] = utils.add_0x_prefix(self._args["_id"].hex())

    # def _parse(self):
    #     self._id = self._event.get("topics")[1].hex()
    #
    #     self._real = int(self._event.get("data"), 16)
    #
    #     self._block_number = self._event.get('blockNumber')
    #     self._transaction = self._event.get('transactionHash').hex()

    def handle(self):
        return []
