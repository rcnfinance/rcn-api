import web3
from contracts.event import EventHandler
from models import Commit


class OwnershipTransferred(EventHandler):
    # event OwnershipTransferred(address indexed _previousOwner, address indexed _newOwner);
    signature = "OwnershipTransferred(address,address)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def handle(self):
        return []