import web3
from contracts.event import EventHandler
from models import Commit


class ClaimedExpired(EventHandler):
    signature = "ClaimedExpired(uint256,uint256,uint256,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def handle(self):
        commit = Commit()

        commit.opcode = "claimed_expired_collateral"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction
        commit.address = self._tx.get("from")

        data = {
            "id": str(self._args.get("_entryId")),
            "auctionId": str(self._args.get("_auctionId")),
            "obligation": str(self._args.get("_obligation")),
            "obligationToken": str(self._args.get("_obligationToken")),
            "status": str(CollateralState.IN_AUCTION.value)
        }

        commit.data = data

        return [commit]
