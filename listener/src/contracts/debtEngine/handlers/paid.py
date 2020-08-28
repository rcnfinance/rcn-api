import web3
from contracts.event import EventHandler
from models import Commit
import utils


class Paid(EventHandler):
    signature = "Paid(bytes32,address,address,uint256,uint256,uint256,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _normalize(self):
        self._args["_id"] = utils.add_0x_prefix(self._args["_id"].hex())

    def handle(self):
        commit = Commit()

        commit.opcode = "paid_debt_engine"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction
        commit.address = self._tx.get("from") if not self._tx is None else None

        data = {
            "id": self._args.get("_id"),
            "sender": self._args.get("_sender"),
            "origin": self._args.get("_origin"),
            "requested": str(self._args.get("_requested")),
            "requested_tokens": str(self._args.get("_requestedTokens")),
            "paid": str(self._args.get("_paid")),
            "tokens": str(self._args.get("_tokens"))
        }

        commit.id_loan = self._args.get("_id")
        commit.data = data

        return [commit]
