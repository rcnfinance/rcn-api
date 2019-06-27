from contracts.event import EventHandler
import web3


class Created(EventHandler):
    signature = "Created(uint256,bytes32,address,uint256,uint32,uint32,uint32,uint32,uint32,uint32)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _normalize(self):
        self._args["_debtId"] = utils.add_0x_prefix(self._args["_debtId"].hex())
        self._args["_token"] = utils.add_0x_prefix(self._args["_token"].hex())

    def handle(self):
        commit = Commit()

        commit.id_entry = self._args.get("_id")
        commit.opcode = "created_entry_collateral"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction
        commit.address = self._tx.get("from")
        commit.data = {
            "id": str(self._args.get("_id")),
            "token": self._args.get("_token"),
            "debtId": self._args.get("_debtId"),
            "amount": str(self._args.get("_amount")),
            "liquidationRatio": str(self._args.get("_liquidationRatio")),
            "balanceRatio": str(self._args.get("_balanceRatio")),
            "burnFee": str(self._args.get("_burnFee")),
            "rewardFee": str(self._args.get("_rewardFee"))
        }

        return [commit]
