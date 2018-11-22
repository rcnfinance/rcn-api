import web3
from contracts.event import EventHandler
from models import Commit
import utils


class Paid(EventHandler):
    signature = "Paid(bytes32,address,address,uint256,uint256,uint256,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _parse(self):
        data = self._event.get("data")
        splited_args = utils.split_every(64, data)

        self._id = self._event.get("topics")[1].hex()

        self._sender = splited_args[0]
        self._origin = splited_args[1]
        self._requested = splited_args[2]
        self._requested_tokens = splited_args[3]
        self._paid = splited_args[4]
        self._tokens = splited_args[5]

        self._block_number = self._event.get('blockNumber')
        self._transaction = self._event.get('transactionHash').hex()

    def handle(self):
        commit = Commit()

        commit.opcode = "paid_debt_engine"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction

        data = {
            "id": self._id,
            "sender": self._sender,
            "origin": self._origin,
            "requested": self._requested,
            "requested_tokens": self._requested_tokens,
            "paid": self._paid,
            "tokens": self._tokens
        }

        commit.data = data

        return [commit]
