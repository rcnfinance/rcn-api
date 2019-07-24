import web3
from contracts.event import EventHandler
from models import Commit
# import utils


class Deposited(EventHandler):
    signature = "Deposited(parameters..)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    # def _normalize(self):
    #     self._args["_id"] = utils.add_0x_prefix(self._args["_id"].hex())

    def handle(self):
        commit = Commit()

        commit.opcode = "deposited_collateral"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction

        data = {
            # "id": self._args.get("_id"),
            # "approved": True
        }

        commit.data = data

        return [commit]
