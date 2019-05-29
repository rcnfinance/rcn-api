import web3
from contracts.event import EventHandler
from models import Commit
from contracts.loanManager.loan_manager import loan_manager_interface
import utils


class Requested(EventHandler):
    signature = "Requested(bytes32,uint128,address,address,address,address,uint256,bytes,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _normalize(self):
        self._args["_id"] = utils.add_0x_prefix(self._args["_id"].hex())
        self._args["_loanData"] = utils.add_0x_prefix(self._args["_loanData"].hex())

    def handle(self):
        commit = Commit()

        commit.opcode = "requested_loan_manager"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction
        commit.address = self._tx.get("from")

        data = {
            "id": self._args.get("_id"),
            "open": True,
            "approved": self._args.get("_creator") == self._args.get("_borrower"),
            "position": "0",
            "expiration": str(self._args.get("_expiration")),
            "amount": str(self._args.get("_amount")),
            "cosigner": "0x0000000000000000000000000000000000000000",
            "model": self._args.get("_model"),
            "creator": self._args.get("_creator"),
            "oracle": self._args.get("_oracle"),
            "borrower": self._args.get("_borrower"),
            "salt": str(self._args.get("_salt")),
            "loanData": self._args.get("_loanData"),
            "created": str(self._block_timestamp()),
            "currency": utils.add_0x_prefix(loan_manager_interface.get_currency(self._args.get("_id"))),
            "status": "0"
        }

        descriptor = loan_manager_interface.get_descriptor(data)

        data["descriptor"] = descriptor

        commit.id_loan = self._args.get("_id")
        commit.data = data

        return [commit]
