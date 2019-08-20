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
        commit.address = self._tx.get("from")
        commit.block_number = self._block_number

        new_data = {
            "previous_owner": self._args.get("_previousOwner"),
            "new_owner": self._args.get("_newOwner"),
        }

        commit.new_data = new_data

        # return [commit]
        return []
