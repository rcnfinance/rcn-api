import web3
from contracts.event import EventHandler
from models import Commit
import utils


class Approved(EventHandler):
    signature = "Approved(bytes32)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _normalize(self):
        self._args["_id"] = utils.add_0x_prefix(self._args["_id"].hex())

    def handle(self):
        commit = Commit()

        commit.opcode = "approved_loan_manager"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction

        data = {
            "id": self._args.get("_id"),
            "approved": True
        }

        commit.id_loan = self._args.get("_id")
        commit.data = data

        return [commit]
