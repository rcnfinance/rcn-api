import os
from contracts.debtModel.debt_model import DebtModel
from ethereum_connection import EthereumConnection
from ethereum_connection import ContractConnection

from .installments_model_interface import InstallmentsModelInterface

ADDRESS = "0x2B1d585520634b4c7aAbD54D73D34333FfFe5c53"

ABI_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "abi.json"
)
URL_NODE = "https://ropsten.node.rcn.loans:8545/"

eth_conn = EthereumConnection(URL_NODE)
contract_connection = ContractConnection(eth_conn, ADDRESS, ABI_PATH)

installments_model_interface = InstallmentsModelInterface(contract_connection)

from .handlers.set_clock import SetClock
from .handlers.set_interest import SetInterest
from .handlers.set_paid_base import SetPaidBase
from .handlers.set_engine import SetEngine
from .handlers.set_descriptor import SetDescriptor
from .handlers.model_handlers import InstallmentsCreated
from .handlers.model_handlers import InstallmentsChangedStatus
from .handlers.model_handlers import InstallmentsAddedPaid

from .commit_processors.installments_added_paid import InstallmentsAddedPaid as InstallmentsAddedPaidCommitProcessor
from .commit_processors.installments_changed_status import InstallmentsChangedStatus as InstallmentsChangedStatusCommitProcessor
from .commit_processors.installments_created import InstallmentsCreated as InstallmentsCreatedCommitProcessor
from .commit_processors.installments_set_clock import InstallmentsSetClock
from .commit_processors.installments_set_interest import InstallmentsSetInterest as InstallmentsSetInterestCommitProcessor
from .commit_processors.installments_set_paid_base import InstallmentsSetPaidBase as InstallmentsSetPaidBaseCommitProcessor

CUSTOM_EVENT_HANDLERS = [
    SetClock,
    SetInterest,
    SetPaidBase,
    SetEngine,
    SetDescriptor,
    InstallmentsCreated,
    InstallmentsChangedStatus,
    InstallmentsAddedPaid
]

commit_processors = [
    InstallmentsAddedPaidCommitProcessor(),
    InstallmentsChangedStatusCommitProcessor(),
    InstallmentsCreatedCommitProcessor(),
    InstallmentsSetClock(),
    InstallmentsSetPaidBaseCommitProcessor(),
    InstallmentsSetInterestCommitProcessor()
]
schedule_processors = []

installments = DebtModel(
    "Installments",
    CUSTOM_EVENT_HANDLERS,
    commit_processors,
    schedule_processors,
    contract_connection
)
