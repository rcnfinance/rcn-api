import web3
from contracts.event import EventHandler
from models import Commit
import utils


class SettledLend(EventHandler):
    signature = "SettledLend(bytes32,address,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _normalize(self):
        self._args["_id"] = utils.add_0x_prefix(self._args["_id"].hex())

    def handle(self):
        commit = Commit()

        commit.opcode = "settled_lend_loan_manager"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction

        data = {
            "id": self._args.get("_id"),
            "lender": self._args.get("_lender"),
            "tokens": self._args.get("_tokens")
        }

        commit.id_loan = self._args.get("_id")
        commit.data = data

        return [commit]
