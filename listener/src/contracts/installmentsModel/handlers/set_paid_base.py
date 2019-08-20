from contracts.event import EventHandler
import web3
import utils
from models import Commit


class SetPaidBase(EventHandler):
    signature = "_setPaidBase(bytes32,uint128)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _normalize(self):
        self._args["_id"] = utils.add_0x_prefix(self._args["_id"].hex())

    def handle(self):
        commit = Commit()

        commit.opcode = "set_paid_base_installments"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction
        commit.address = self._tx.get("from")
        commit.block_number = self._block_number

        data = {
            "id": self._args.get("_id"),
            "paid_base": str(self._args.get("_paidBase"))
        }

        commit.id_loan = self._args.get("_id")
        commit.new_data = data

        return [commit]
