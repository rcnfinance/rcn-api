import web3
from contracts.event import EventHandler
from models import Commit


class ReadedOracle(EventHandler):
    signature = "ReadedOracle(address,uint256,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def handle(self):
        commit = Commit()

        commit.opcode = "readed_oracle_collateral"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction

        data = {
            "oracle": self._args.get("_oracle"),
            "tokens": self._args.get("_tokens"),
            "equivalent": self._args.get("_equivalent")
        }

        commit.data = data

        return []
