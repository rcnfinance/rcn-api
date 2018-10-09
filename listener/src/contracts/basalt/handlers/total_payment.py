import web3
from .event_handler import EventHandler
import utils
from ..models import Commit

class TotalPayment(EventHandler):
    signature = 'TotalPayment(uint256)'
    signature_hash = web3.Web3.sha3(text=signature)

    def _parse(self):
        data = self._event.get('data')[2:]
        splited_args = utils.split_every(64, data)
        self._index = utils.to_int(splited_args[0])
        self._block_number = self._event.get('blockNumber')
        self._transaction = self._event.get('transactionHash').hex()

    def do(self):
        self._logger.info("Apply handler")
        commit = Commit()
        block_timestamp = self._block_timestamp()

        data = {}
        data['loan'] = self._index

        commit.opcode = "total_payment"
        commit.timestamp = block_timestamp
        commit.proof = self._transaction
        commit.data = data
        # commit.loan = loan.to_dict()

        return [commit]
