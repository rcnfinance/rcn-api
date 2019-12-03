import web3
from contracts.event import EventHandler
from models import Commit


class StartedAuction(EventHandler):
    signature = "StartedAuction(uint256,uint256,uint256,uint256,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def handle(self):
        commit = Commit()

        commit.opcode = "started_auction"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction
        commit.address = self._tx.get("from")

        data = {
            "id": str(self._args.get("_entryId")),
            "startOffer": str(self._args.get("_startOffer")),
            "referenceOffer": str(self._args.get("_referenceOffer")),
            "limit": str(self._args.get("_limit")),
            "required": str(self._args.get("_required")),
        }

        commit.data = data

        return [commit]
