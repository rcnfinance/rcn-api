import web3
from contracts.event import EventHandler
import utils
from models import Commit
from contracts.debtEngine.debt_engine import debt_engine_interface


class Created2(EventHandler):
    signature = "Created2(bytes32,uint256,bytes)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _parse(self):
        print(self._event)
        data = self._event.get("data")[2:]
        splited_args = utils.split_every(64, data)
        self._id = splited_args[0]
        self._nonce = splited_args[1]
        self._data = splited_args[2]
        self._block_number = self._event.get('blockNumber')
        self._transaction = self._event.get('transactionHash').hex()

    def handle(self):
        commit = Commit()

        commit.opcode = "created_debt"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction

        debt = debt_engine_interface.get_debt_by_id(self._id)

        error = debt[0]
        currency = debt[1].hex()
        balance = debt[2]
        model = debt[3]
        creator = debt[4]
        oracle = debt[5]

        data = {
            "_data": self._data,
            "error": error,
            "currency": currency,
            "balance": str(balance),
            "model": model,
            "creator": creator,
            "oracle": oracle,
            "id": self._id
        }

        commit.data = data

        return [commit]