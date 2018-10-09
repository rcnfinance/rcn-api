import web3
from .event_handler import EventHandler
import utils
from ..models import Commit

class DestroyedBy(EventHandler):
    signature = 'DestroyedBy(uint256,address)'
    signature_hash = web3.Web3.sha3(text=signature)

    def _parse(self):
        data = self._event.get('data')[2:]
        splited_args = utils.split_every(64, data)
        self._index = utils.to_int(splited_args[0])
        self._address = utils.to_address(splited_args[1])
        self._block_number = self._event.get('blockNumber')
        self._transaction = self._event.get('transactionHash').hex()

    def do(self):
        self._logger.info("Apply handler")
        commit = Commit()

        data = {}
        data['loan'] = self._index
        data['destroyed_by'] = self._address

        commit.opcode = "destroyed_loan"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction
        commit.data = data

        return [commit]
