import web3
from contracts.event import EventHandler
from models import Commit
# import utils

class PoolCreated(EventHandler):
    signature = "PoolCreated(bytes32,address,bytes32,address,uint256,bytes,address,address)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    # def _normalize(self):
    #     self._args["_id"] = utils.add_0x_prefix(self._args["_id"].hex())

    def handle(self):
        commit = Commit()

        commit.opcode = "pool_created_loanDAO"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction

        data = {
            "poolId": self._args.get("_poolId"),
            "manager": self._args.get("_manager"),
            "loanId": self._args.get("_loanId"),
            "cosigner": self._args.get("_cosigner"),
            "cosignerLimit": self._args.get("_cosignerLimit"),
            "cosignerData": self._args.get("_cosignerData"),
            "started": False,
            "token": self._args.get("_token"),
            "tracker": self._args.get("_tracker"),
            "raised": "0",
            "collected": "0"
        }

        commit.data = data

        return [commit]
