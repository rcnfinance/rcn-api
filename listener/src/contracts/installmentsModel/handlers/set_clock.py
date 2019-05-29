from contracts.event import EventHandler
import web3
import utils
from models import Commit


class SetClock(EventHandler):
    signature = "_setClock(bytes32,uint64)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _normalize(self):
        self._args["_id"] = utils.add_0x_prefix(self._args["_id"].hex())

    def handle(self):
        commit = Commit()

        commit.opcode = "set_clock_installments"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction

        data = {
            "id": self._args.get("_id"),
            "duration": str(self._args.get("_to"))
        }

        commit.id_loan = self._args.get("_id")
        commit.data = data

        return [commit]
