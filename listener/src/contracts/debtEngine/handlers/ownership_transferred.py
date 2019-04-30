import web3
from contracts.event import EventHandler
from models import Commit


class OwnershipTransferred(EventHandler):
    # event OwnershipTransferred(address indexed _previousOwner, address indexed _newOwner);
    signature = "OwnershipTransferred(address,address)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def handle(self):
        commit = Commit()

        commit.opcode = "ownership_transferred_debt_engine"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction

        data = {
            "previous_owner": self._args.get("_previousOwner"),
            "new_owner": self._args.get("_newOwner"),
        }

        commit.data = data

        # return [commit]
        return []
