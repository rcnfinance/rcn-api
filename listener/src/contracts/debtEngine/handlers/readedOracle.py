import web3
from contracts.event import EventHandler


class ReadedOracle(EventHandler):
    signature = "ReadedOracle(bytes32,address,bytes32,uint256,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _parse(self):
        pass

    def handle(self):
        return []