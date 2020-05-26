import web3
from contracts.event import EventHandler
from models import Commit
from contracts.debtEngine.debt_engine import debt_engine_interface
import utils

class Transfer(EventHandler):
    signature = "Transfer(address,address,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _normalize(self):
        self._args["_tokenId"] = self._event.get("topics")[3].hex()
     
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
            commit = Commit()

            commit.opcode = "created_debt_engine"
            commit.timestamp = self._block_timestamp()
            commit.proof = self._transaction
            commit.address = self._tx.get("from")

            self._id = self._args.get("_tokenId")

            debt = debt_engine_interface.get_debt_by_id(self._id)

            error = False
            balance = 0

            model = debt.get("model")
            creator = debt.get("creator")
            oracle = debt.get("oracle")

            created = str(self._block_timestamp())

            data = {
                "error": error,
                "balance": str(balance),
                "model": model,
                "creator": creator,
                "oracle": oracle,
                "created": created,
                "id": self._id,
                "from": self._args.get("_from"),
                "to": self._args.get("_to")
            }

            commit.id_loan = self._id
            commit.data = data

            return [commit]
