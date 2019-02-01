import web3
from contracts.event import EventHandler
from models import Commit
from contracts.debtEngine.debt_engine import debt_engine_interface


class Created3(EventHandler):
    signature = "Created3(bytes32,uint256,bytes)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    # def _parse(self):
    #     self._data = self._event.get("data")
    #     self._id = self._event.get("topics")[1].hex()
    #     self._block_number = self._event.get('blockNumber')
    #     self._transaction = self._event.get('transactionHash').hex()

    def _normalize(self):
        self._args["_id"] = utils.add_0x_prefix(self._args["_id"].hex())

    def handle(self):
        commit = Commit()

        commit.opcode = "created_debt_engine"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction

        debt = debt_engine_interface.get_debt_by_id(self._id)

        error = False
        balance = 0
        model = debt.get("model")
        creator = debt.get("creator")
        oracle = debt.get("oracle")
        created = str(self._block_timestamp())

        data = {
            "_data": self._args.get("data"),
            "error": error,
            "balance": str(balance),
            "model": model,
            "creator": creator,
            "oracle": oracle,
            "created": created,
            "id": self._args.get("_id")
        }

        commit.data = data

        return [commit]
