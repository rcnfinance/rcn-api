import web3
from .event_handler import EventHandler
from handlers import utils
from models import Commit

class TransferHandler(EventHandler):
    signature = 'Transfer(address,address,uint256)'
    signature_hash = web3.Web3.sha3(text=signature)

    def _parse(self):
        data = self._event.get('data')[2:]
        self._from = utils.to_address(web3.Web3.toHex(self._event.get("topics")[1]))
        self._to = utils.to_address(web3.Web3.toHex(self._event.get("topics")[2]))
        self._index = utils.to_int(data)
        self._transaction = self._event.get('transactionHash').hex()
        self._block_number = self._event.get('blockNumber')

    def do(self):
        commit = Commit()

        data = {}
        data['loan'] = self._index
        data['to'] = self._to
        data['from'] = self._from

        commit.opcode = "transfer"
        commit.timestamp = str(self._w3.eth.getBlock(self._block_number).timestamp)
        commit.proof = self._transaction
        commit.data = data

        return [commit]
