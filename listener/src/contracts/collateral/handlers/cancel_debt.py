import web3
from contracts.event import EventHandler
from models import Commit


class CancelDebt(EventHandler):
    signature = "CancelDebt(uint256,uint256,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def handle(self):
        commit = Commit()

        commit.opcode = "cancel_debt_collateral"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction
        commit.address = self._tx.get("from")

        data = {
            "id": str(self._args.get("_entryId")),
            "obligationInToken": str(self._args.get("_obligationInToken")),
            "payTokens": str(self._args.get("_payTokens"))
        }

        commit.data = data

        return [commit]