import web3
from contracts.event import EventHandler
from models import Commit


class TakeFee(EventHandler):
    signature = "TakeFee(uint256,uint256,address,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def handle(self):
        commit = Commit()

        commit.opcode = "take_fee_collateral"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction
        commit.address = self._tx.get("from")

        data = {
            "id": str(self._args.get("_entryId")),
            "burned": str(self._args.get("_burned")),
            "rewarTo": self._args.get("_rewardTo"),
            "rewarded": str(self._args.get("_rewarded")),
        }

        commit.data = data

        return []
