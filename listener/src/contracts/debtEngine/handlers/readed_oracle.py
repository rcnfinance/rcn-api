import web3
from contracts.event import EventHandler
from models import Commit
import utils


class ReadedOracle(EventHandler):
    signature = "ReadedOracle(bytes32,uint256,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def handle(self):
        return []
