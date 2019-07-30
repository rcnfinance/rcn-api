import web3
from contracts.event import EventHandler
from models import Commit
import utils


class Created(EventHandler):
    signature = "Created(uint256,bytes32,address,address,uint256,uint32,uint32,uint32,uint32)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _normalize(self):
        self._args["_debtId"] = utils.add_0x_prefix(self._args["_debtId"].hex())
      

    def handle(self):
        commit = Commit()

        commit.opcode = "created_collateral"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction
        commit.id_loan = self._args.get("_debtId")
        commit.address = self._tx.get("from")

        data = {
            "id": str(self._args.get("_id")),
            "debt_id": self._args.get("_debtId"),
            "oracle": self._args.get("_oracle"),
            "token": self._args.get("_token"),
            "amount": str(self._args.get("_amount")),
            "liquidation_ratio": str(self._args.get("_liquidationRatio")),
            "balance_ratio": str(self._args.get("_balanceRatio")),
            "burn_fee": str(self._args.get("_burnFee")),  
            "reward_fee": str(self._args.get("_rewardFee")),
            "started": False,  
            "invalid": False
        }

        commit.data = data

        return [commit]
