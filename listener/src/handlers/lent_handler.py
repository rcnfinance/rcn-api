import web3

from .event_handler import EventHandler
from handlers import utils
from models import Commit
from models import Loan

class LentHandler(EventHandler):
    signature = 'Lent(uint256,address,address)'
    signature_hash = web3.Web3.sha3(text=signature)

    def _parse(self):
        data = self._event.get('data')[2:]
        splited_args = utils.split_every(64, data)
        self._index = utils.to_int(splited_args[0])
        self._lender = utils.to_address(splited_args[1])
        self._cosigner = utils.to_address(splited_args[2])
        self._block_number = self._event.get('blockNumber')
        self._transaction = self._event.get('transactionHash').hex()

    def do(self):
        loan = Loan.objects(index=self._index).first()
        block_timestamp = self._w3.eth.getBlock(self._block_number).timestamp
        commit = Commit()

        data = {}
        data['lender'] = self._lender
        data['loan'] = self._index
        data["due_time"] = str(block_timestamp + int(loan.dues_in))

        commit.opcode = "lent"
        commit.timestamp = str(block_timestamp)
        commit.proof = self._transaction
        commit.data = data
        return [commit]
    