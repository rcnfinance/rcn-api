import os
from contract import Contract
from ethereum_connection import EthereumConnection
from ethereum_connection import ContractConnection

from .handlers.approval import Approval
from .handlers.approval_for_all import ApprovalForAll
from .handlers.approved_by import ApprovedBy
from .handlers.created_loan import CreatedLoan
from .handlers.destroyed_by import DestroyedBy
from .handlers.lent import Lent
from .handlers.partial_payment import PartialPayment
from .handlers.total_payment import TotalPayment
from .handlers.transfer import Transfer

from .commit_processors.approved_loan_commit_processor import ApprovedLoanCommitProcessor
from .commit_processors.destroyed_loan_commit_processor import DestroyedLoanCommitProcessor
from .commit_processors.interest_commit_processor import InterestCommitProcessor
from .commit_processors.lent_commit_processor import LentCommitProcessor
from .commit_processors.loan_expired_commit_processor import LoanExpiredCommitProcessor
from .commit_processors.loan_in_debt_commit_processor import LoanInDebtCommitProcessor
from .commit_processors.loan_request_commit_processor import LoanRequestCommitProcessor
from .commit_processors.partial_payment_commit_processor import PartialPaymentCommitProcessor
from .commit_processors.total_payment_commit_processor import TotalPaymentCommitProcessor
from .commit_processors.transfer_commit_processor import TransferCommitProcessor

from .schedule_processors.check_expired_schedule_processor import CheckExpiredScheduleProcessor
from .schedule_processors.check_in_debt_schedule_processor import CheckInDebtScheduleProcessor


URL_NODE = "https://ropsten.node.rcn.loans:8545/"
CONTRACT_ADDRESS = '0xbeE217bfe06C6FAaa2d5f2e06eBB84C5fb70d9bF'
ABI_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "abi.json"
)

event_handlers = [
    Approval,
    ApprovalForAll,
    ApprovedBy,
    CreatedLoan,
    DestroyedBy,
    Lent,
    PartialPayment,
    TotalPayment,
    Transfer
]

commit_processors = [
    ApprovedLoanCommitProcessor(), 
    DestroyedLoanCommitProcessor(), 
    InterestCommitProcessor(), 
    LentCommitProcessor(), 
    LoanExpiredCommitProcessor(), 
    LoanInDebtCommitProcessor(), 
    LoanRequestCommitProcessor(), 
    PartialPaymentCommitProcessor(), 
    TotalPaymentCommitProcessor(), 
    TransferCommitProcessor()
]

schedule_processors = [
    CheckExpiredScheduleProcessor(),
    CheckInDebtScheduleProcessor()
]
ethereum_connection = EthereumConnection(URL_NODE)
contract_connection = ContractConnection(
    ethereum_connection,
    CONTRACT_ADDRESS,
    ABI_PATH
)

basalt = Contract(
    'BASALT',
    event_handlers,
    commit_processors,
    schedule_processors,
    contract_connection
)