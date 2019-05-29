import web3
from contracts.event import EventHandler
from models import Commit
import utils


class SettledCancel(EventHandler):
    signature = "SettledCancel(bytes32,address)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _normalize(self):
        self._args["_id"] = utils.add_0x_prefix(self._args["_id"].hex())

    def handle(self):
        commit = Commit()

        commit.opcode = "settled_cancel_loan_manager"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction
        commit.address = self._tx.get("from")

        data = {
            "id": self._args.get("_id"),
            "cancel": self._args.get("_canceler"),
        }

        commit.id_loan = self._args.get("_id")
        commit.data = data

        return [commit]
