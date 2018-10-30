import os
from contracts.debtModel.debt_model import DebtModel
from ethereum_connection import EthereumConnection
from ethereum_connection import ContractConnection

from .handlers.set_clock import SetClock
from .handlers.set_interest import SetInterest
from .handlers.set_paid_base import SetPaidBase
from .handlers.set_status import SetStatus

ADDRESS = "0x3dF10D67F683FE26a9f658b99e3C6a4a94d20690"
ABI_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "abi.json"
)
URL_NODE = "https://ropsten.node.rcn.loans:8545/"

CUSTOM_EVENT_HANDLERS = [
    SetClock,
    SetInterest,
    SetPaidBase,
    SetStatus
]

commit_processors = []
schedule_processors = []

eth_conn = EthereumConnection(URL_NODE)
contract_connection = ContractConnection(eth_conn, ADDRESS, ABI_PATH)

installments = DebtModel(
    "Installments",
    CUSTOM_EVENT_HANDLERS,
    commit_processors,
    schedule_processors,
    contract_connection
)