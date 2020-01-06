import web3
from contracts.event import EventHandler
from models import Commit


class ClaimedLiquidation(EventHandler):
    signature = "ClaimedLiquidation(uint256,uint256,uint256,uint256,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def handle(self):
        commit = Commit()

        commit.opcode = "claimed_liquidation_collateral"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction
        commit.address = self._tx.get("from")

        data = {
            "id": str(self._args.get("_entryId")),
            "auctionId": str(self._args.get("_auctionId")),
            "debt": str(self._args.get("_debt")),
            "required": str(self._args.get("_required")),
            "marketValue": str(self._args.get("_marketValue")),
        }

        commit.data = data

        return [commit]
