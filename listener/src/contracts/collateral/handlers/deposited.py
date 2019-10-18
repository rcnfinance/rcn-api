import web3
from contracts.event import EventHandler
from models import Commit
# import utils


class Deposited(EventHandler):
    signature = "Deposited(uint256,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    # def _normalize(self):
    #     self._args["_entryId"] = utils.add_0x_prefix(self._args["_entryId"].hex())

    def handle(self):
        commit = Commit()

        commit.opcode = "deposited_collateral"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction
        commit.address = self._tx.get("from")

        data = {
            "id": str(self._args.get("_entryId")),
            "amount": str(self._args.get("_amount")),
        }

        commit.data = data

        return [commit]
