import web3
from contracts.event import EventHandler
from models import Commit
import utils


class Paid(EventHandler):
    signature = "Paid(bytes32,address,address,uint256,uint256,uint256,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _parse(self):
        data = self._event.get("data")[2:]
        splited_args = utils.split_every(64, data)

        self._id = self._event.get("topics")[1].hex()

        self._sender = "0x" + splited_args[0][24:]
        self._origin = "0x" + splited_args[1][24:]
        self._requested = int(splited_args[2], 16)
        self._requested_tokens = int(splited_args[3], 16)
        self._paid = int(splited_args[4], 16)
        self._tokens = int(splited_args[5], 16)

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
            "requested": str(self._requested),
            "requested_tokens": str(self._requested_tokens),
            "paid": str(self._paid),
            "tokens": str(self._tokens)
        }

        commit.data = data

        return [commit]
