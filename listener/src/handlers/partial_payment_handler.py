import web3
from .event_handler import EventHandler
from handlers import utils
from models import Commit

class PartialPaymentHandler(EventHandler):
    signature = 'PartialPayment(uint256,address,address,uint256)'
    signature_hash = web3.Web3.sha3(text=signature)

    def _parse(self):
        data = self._event.get('data')[2:]
        splited_args = utils.split_every(64, data)
        self._index = utils.to_int(splited_args[0])
        self._sender = utils.to_address(splited_args[1])
        self._from = utils.to_address(splited_args[2])
        self._amount = str(utils.to_int(splited_args[3]))
        self._block_number = self._event.get('blockNumber')
        self._transaction = self._event.get('transactionHash').hex()

    def do(self):
        commit = Commit()

        data = {}
        data['loan'] = self._index
        data['sender'] = self._sender
        data['from'] = self._from
        data['amount'] = self._amount

        commit.opcode = "partial_payment"
        commit.timestamp = str(self._w3.eth.getBlock(self._block_number).timestamp)
        commit.proof = self._transaction
        commit.data = data

        return [commit]
