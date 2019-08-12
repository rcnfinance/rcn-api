import web3
from contracts.event import EventHandler
from models import Commit
# import utils


class Provide(EventHandler):
    signature = "Provide(address,address,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    # def _normalize(self):
    #     self._args["_id"] = utils.add_0x_prefix(self._args["_id"].hex())

    def handle(self):
        commit = Commit()

        commit.opcode = "provide_oracleFactory"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction
        commit.address = self._tx.get("from")

        data = {
            "oracle": self._args.get("_oracle"),
            "signer": self._args.get("_signer"),
            "rate": str(self._args.get("_rate"))
        }

        commit.data = data

        return [commit]