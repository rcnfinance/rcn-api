import web3
from .event_handler import EventHandler
from handlers import utils
from models import Commit

class ApprovedByHandler(EventHandler):
    signature = 'ApprovedBy(uint256,address)'
    signature_hash = web3.Web3.sha3(text=signature)

    def _parse(self):
        data = self._event.get('data')[2:]
        splited_args = utils.split_every(64, data)
        self._index = utils.to_int(splited_args[0])
        self._address = utils.to_address(splited_args[1])
        self._block_number = self._event.get('blockNumber')
        self._transaction = str(self._event.get('transactionHash'))

    def do(self):
        commit = Commit()

        data = {}
        data['loan'] = self._index
        data['approved_by'] = self._address

        commit.opcode = "approved_loan"
        commit.timestamp = self._w3.eth.getBlock(self._block_number).timestamp
        commit.proof = self._transaction
        commit.data = data

        return [commit]