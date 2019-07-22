import web3
from contracts.event import EventHandler
from models import Commit
# import utils


class PayBack(EventHandler):
    signature = "PayBack(bytes32,address,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    # def _normalize(self):
    #     self._args["_id"] = utils.add_0x_prefix(self._args["_id"].hex())

    def handle(self):
        commit = Commit()

        commit.opcode = "pay_back_loanDAO"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction

        data = {
            "poolId": self._args.get("_poolId"),
            "lender": self._args.get("_lender"),
            "rest": str(self._args.get("_rest"))
        }

        commit.data = data

        return [commit]
