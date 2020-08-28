import web3
from contracts.event import EventHandler
from models import Commit
import utils


class Withdrawn(EventHandler):
    signature = "Withdrawn(bytes32,address,address,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _normalize(self):
        self._args["_id"] = utils.add_0x_prefix(self._args["_id"].hex())

    def handle(self):
        commit = Commit()

        commit.opcode = "withdrawn_debt_engine"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction
        commit.address = self._tx.get("from") if not self._tx is None else None

        data = {
            "id": self._args.get("_id"),
            "sender": self._args.get("_sender"),
            "to": self._args.get("_to"),
            "amount": str(self._args.get("_amount"))
        }

        commit.id_loan = self._args.get("_id")
        commit.data = data

        return [commit]
