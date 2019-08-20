from contracts.debtModel.handlers.added_debt import AddedDebt
from contracts.debtModel.handlers.added_paid import AddedPaid
from contracts.debtModel.handlers.changed_due_time import ChangedDueTime
from contracts.debtModel.handlers.changed_final_time import ChangedFinalTime
from contracts.debtModel.handlers.changed_frecuencalcy import ChangedFrecuencalcy
from contracts.debtModel.handlers.changed_obligation import ChangedObligation
from contracts.debtModel.handlers.changed_status import ChangedStatus
from contracts.debtModel.handlers.created import Created

from contracts.installmentsModel.installments import installments_model_interface

from models import Commit
from models import State
import utils


class InstallmentsAddedDebt(AddedDebt):
    def handle(self):
        return []


class InstallmentsAddedPaid(AddedPaid):
    def _normalize(self):
        self._args["_id"] = utils.add_0x_prefix(self._args["_id"].hex())

    def handle(self):
        commit = Commit()

        commit.opcode = "added_paid_installments"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction
        commit.address = self._tx.get("from")
        commit.block_number = self._block_number

        state = State.objects.get(id=self._args.get("_id"))

        new_data = {
            "id": self._args.get("_id"),
            "real": str(self._args.get("_paid")),
            "paid": str(int(state.paid) + self._args.get("_paid")),
            "state_last_payment": state.clock,
        }

        commit.id_loan = self._args.get("_id")
        commit.new_data = new_data

        return [commit]


class InstallmentsChangedDueTime(ChangedDueTime):
    def handle(self):
        return []


class InstallmentsChangedFinalTime(ChangedFinalTime):
    def handle(self):
        return []


class InstallmentsChangedFrecuencalcy(ChangedFrecuencalcy):
    def handle(self):
        return []


class InstallmentsChangedObligation(ChangedObligation):
    def handle(self):
        return []


class InstallmentsChangedStatus(ChangedStatus):
    def _normalize(self):
        self._args["_id"] = utils.add_0x_prefix(self._args["_id"].hex())

    def handle(self):
        commits = []

        commit = Commit()

        commit.opcode = "changed_status_installments"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction
        commit.address = self._tx.get("from")
        commit.block_number = self._block_number

        new_data = {
            "id": self._args.get("_id"),
            "timestamp": str(self._args.get("_timestamp")),
            "status": str(self._args.get("_status"))
        }

        commit.id_loan = self._args.get("_id")
        commit.new_data = new_data
        commits.append(commit)

        # commit full payment loan manager
        commit_full_payment = Commit()
        commit_full_payment.opcode = "full_payment_loan_manager"
        commit_full_payment.timestamp = commit.timestamp
        commit_full_payment.proof = self._transaction
        commit_full_payment.address = self._tx.get("from")
        commit_full_payment.block_number = self._block_number

        new_data = {
            "id": self._args.get("_id"),
            "status": str(self._args.get("_status"))
        }

        commit_full_payment.id_loan = self._args.get("_id")
        commit_full_payment.new_data = new_data

        commits.append(commit_full_payment)

        return commits


class InstallmentsCreated(Created):
    def _normalize(self):
        self._args["_id"] = utils.add_0x_prefix(self._args["_id"].hex())

    def handle(self):
        commit = Commit()

        config_data = installments_model_interface.get_config_by_id(self._args.get("_id"))

        commit.opcode = "created_installments"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction
        commit.address = self._tx.get("from")
        commit.block_number = self._block_number
        commit.new_data = config_data
        commit.id_loan = self._args.get("_id")

        return [commit]
