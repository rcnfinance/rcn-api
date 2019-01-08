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

class InstallmentsAddedDebt(AddedDebt):
    def handle(self):
        return []


class InstallmentsAddedPaid(AddedPaid):
    def handle(self):
        commit = Commit()

        commit.opcode = "added_paid_installments"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction

        state = State.objects.get(id=self._id)

        data = {
            "id": self._id,
            "real": str(self._real),
            "paid": str(state.paid + self._real),
            "state_last_payment": state.clock,
        }

        commit.data = data

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
    def handle(self):
        commit = Commit()

        commit.opcode = "changed_status_installments"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction

        data = {
            "id": self._id,
            "timestamp": self._timestamp,
            "status": str(self._status)
        }

        commit.data = data
        return [commit]


class InstallmentsCreated(Created):
    def handle(self):
        commit = Commit()

        config = installments_model_interface.get_config_by_id(self._id)

        print(config)

        data = {
            "installments": config[0],
            "timeUnit": config[1],
            "duration": config[2],
            "lentTime": config[3],
            "cuota": int(config[4]),
            "interestRate": int(config[5]),
            "id": self._id,
        }

        commit.opcode = "created_installments"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction
        commit.data = data

        return [commit]
