import web3
from contracts.event import EventHandler
from models import Commit


class SetMaxSpreadRatio(EventHandler):
    signature = "SetMaxSpreadRatio(address,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def handle(self):
        commit = Commit()

        commit.opcode = "set_max_spread_ratio"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction

        data = {
            "token": self._args.get("_token"),
            "maxSpreadRatio": self._args.get("_maxSpreadRatio")
        }

        commit.data = data

        return []
