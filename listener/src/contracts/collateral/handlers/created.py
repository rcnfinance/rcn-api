import web3
from contracts.event import EventHandler
from models import Commit
# import utils


class Created(EventHandler):
    signature = "Created(uint256,bytes32,address,uint256,uint32,uint32,uint32,uint32)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    # def _normalize(self):
    #     self._args["_id"] = utils.add_0x_prefix(self._args["_id"].hex())

    def handle(self):
        commit = Commit()

        commit.opcode = "created_collateral"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction

        data = {
            "id": self._args.get("_id"),
            "debt_id": self._args.get("_debtId"),
            "token": self._args.get("_token"),
            "amount": self._args.get("_amount"),
            "liquidation_ratio": self._args.get("_liquidationRatio"),
            "balance_ratio": self._args.get("_balanceRatio"),
            "burn_fee": self._args.get("_burnFee"),  
            "reward_fee": self._args.get("_rewardFee"),  
        }

        commit.data = data

        return [commit]
