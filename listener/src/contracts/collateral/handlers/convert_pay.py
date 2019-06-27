from contracts.event import EventHandler
import web3


class ConvertPay(EventHandler):
    signature = "ConvertPay(uint256,uint256,bytes)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def handle(self):
        return []
