from .approval_for_all_handler import ApprovalForAllHandler
from .approval_handler import ApprovalHandler
from .approved_by_handler import ApprovedByHandler
from .created_loan_handler import CreatedLoanHandler
from .destroyed_by_handler import DestroyedByHandler
from .lent_handler import LentHandler
from .partial_payment_handler import PartialPaymentHandler
from .total_payment_handler import TotalPaymentHandler
from .transfer_handler import TransferHandler


def get_class_by_event(event):
    events = [
        ApprovalForAllHandler,
        ApprovalHandler,
        ApprovedByHandler,
        CreatedLoanHandler,
        DestroyedByHandler,
        LentHandler,
        PartialPaymentHandler,
        TotalPaymentHandler,
        TransferHandler
    ]
    hash_signature_event = {event_class.signature_hash: event_class for event_class in events}

    return hash_signature_event.get(event.get('topics')[0])(event)