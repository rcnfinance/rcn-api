from .handlers.added_debt import AddedDebt
from .handlers.added_paid import AddedPaid
from .handlers.changed_due_time import ChangedDueTime
from .handlers.changed_final_time import ChangedFinalTime
from .handlers.changed_frecuencalcy import ChangedFrecuencalcy
from .handlers.changed_obligation import ChangedObligation
from .handlers.changed_status import ChangedStatus
from .handlers.created import Created
from .handlers.ownership_transferred import OwnershipTransferred
from contract import Contract


BASE_EVENTS_HANDLERS = [
    AddedDebt,
    AddedPaid,
    ChangedDueTime,
    ChangedFinalTime,
    ChangedFrecuencalcy,
    ChangedObligation,
    ChangedStatus,
    Created,
    OwnershipTransferred
]


class DebtModel(Contract):
    def __init__(self, name, address, abi_path, event_handlers, commit_processors, schedule_processors):
        map_signature_handler = {handler.signature: handler for handler in event_handlers}
        for base_handler in BASE_EVENTS_HANDLERS:
            if base_handler.signature not in map_signature_handler:
                map_signature_handler[base_handler.signature] = base_handler

        super().__init__(
            name,
            address,
            abi_path,
            list(map_signature_handler.values()),
            commit_processors,
            schedule_processors
        )
