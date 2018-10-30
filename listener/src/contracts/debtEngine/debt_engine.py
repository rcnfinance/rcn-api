import os
from contract import Contract
from ethereum_connection import EthereumConnection
from ethereum_connection import ContractConnection

from .debt_engine_interface import DebtEngineInterface


ADDRESS = "0x2a878750a122EC3D6a193A4C6003Ecd8E98feB17"
ABI_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "abi.json"
)
URL_NODE = "https://ropsten.node.rcn.loans:8545/"

eth_conn = EthereumConnection(URL_NODE)
contract_connection = ContractConnection(eth_conn, ADDRESS, ABI_PATH)

debt_engine_interface = DebtEngineInterface(contract_connection)

from .handlers.created import Created
from .handlers.created2 import Created2
from .handlers.paid import Paid
from .handlers.readedOracle import ReadedOracle
from .handlers.withdrawn import Withdrawn
from .handlers.approval import Approval
from .handlers.approval_for_all import ApprovalForAll
from .handlers.transfer import Transfer
from .handlers.set_descriptor import SetDescriptor
from .handlers.set_engine import SetEngine

from .commit_processors.created_debt import CreatedDebt

commit_processors = [CreatedDebt()]
schedule_processors = []

EVENTS_HANDLERS = [
    Approval,
    ApprovalForAll,
    Created,
    Created2,
    Paid,
    ReadedOracle,
    Withdrawn,
    Transfer,
    SetEngine,
    SetDescriptor
]


debt_engine = Contract(
    "DebtEngine",
    EVENTS_HANDLERS,
    commit_processors,
    schedule_processors,
    contract_connection
)
