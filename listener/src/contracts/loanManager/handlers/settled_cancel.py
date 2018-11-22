import web3
from contracts.event import EventHandler
from models import Commit


class SettledCancel(EventHandler):
    signature = "SettledCancel(bytes32,address)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _parse(self):
        self._id = self._event.get("topics")[1].hex()
        self._canceler = self._event.get("data")
        self._block_number = self._event.get('blockNumber')
        self._transaction = self._event.get('transactionHash').hex()

    def handle(self):
        commit = Commit()

        commit.opcode = "settled_cancel_loan_manager"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction

        data = {
            "id": self._id,
            "cancel": self._cancel,
        }

        commit.data = data

        return [commit]
