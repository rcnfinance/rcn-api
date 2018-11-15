from contracts.event import EventHandler
import web3
import utils


class ChangedStatus(EventHandler):
    signature = "ChangedStatus(bytes32,uint256,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _parse(self):
        self._id = self._event.get("topics")[1]

        data = self._event.get("data")[2:]
        splited_args = utils.split_every(64, data)
        self._timestamp = splited_args[1]
        self._status = splited_args[2]

        self._block_number = self._event.get('blockNumber')
        self._transaction = self._event.get('transactionHash').hex()

    def handle(self):
        return []