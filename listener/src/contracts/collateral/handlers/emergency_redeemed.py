import web3
from contracts.event import EventHandler
from models import Commit
# import utils


class EmergencyRedeemed(EventHandler):
    signature = "EmergencyRedeemed(uint256,address)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    # def _normalize(self):
    #     self._args["_id"] = utils.add_0x_prefix(self._args["_id"].hex())

    def handle(self):
        commit = Commit()

        commit.opcode = "emergency_redeemed_collateral"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction
        commit.address = self._tx.get("from")

        data = {
            "id": str(self._args.get("_id")),
            "to": str(self._args.get("_to"))
        }

        commit.data = data

        return [commit]
