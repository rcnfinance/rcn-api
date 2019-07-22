import web3
from contracts.event import EventHandler
from models import Commit
import utils

class Transfer(EventHandler):
    signature = "Transfer(address,address,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _normalize(self):
        self._args["_tokenId"] = hex(self._args["_tokenId"])
     

    def handle(self):
        if self._args.get("_from") != "0x0000000000000000000000000000000000000000":

            commit = Commit()

            commit.opcode = "transfer_debt_engine"
            commit.timestamp = self._block_timestamp()
            commit.proof = self._transaction
            commit.address = self._tx.get("from")

            data = {
                "id": self._args.get("_tokenId"),
                "from": self._args.get("_from"),
                "to": self._args.get("_to")
            }

            commit.id_loan = self._args.get("_tokenId")
            commit.data = data

            return [commit]
        else:
            return []
