from contracts.event import EventHandler
import web3


class EmergencyRedeemed(EventHandler):
    signature = "EmergencyRedeemed(uint256,address)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def handle(self):
        return []
