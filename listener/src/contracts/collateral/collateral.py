import os
from contract import Contract
from ethereum_connection import EthereumConnection
from ethereum_connection import ContractConnection


ADDRESS = os.environ.get("COLLATERAL_ADDRESS")

ABI_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "abi.json"
)
URL_NODE = os.environ.get("URL_NODE")


eth_conn = EthereumConnection(URL_NODE)
contract_connection = ContractConnection(eth_conn, ADDRESS, ABI_PATH)

from .handlers.cancel_debt import CancelDebt
from .handlers.collateral_balance import CollateralBalance
from .handlers.convert_pay import ConvertPay
from .handlers.created import Created
from .handlers.deposited import Deposited
from .handlers.emergency_redeemed import EmergencyRedeemed
from .handlers.pay_off_debt import PayOffDebt
from .handlers.rebuy import Rebuy
from .handlers.redeemed import Redeemed
from .handlers.set_burner import SetBurner
from .handlers.set_converter import SetConverter
from .handlers.set_url import SetUrl
from .handlers.started import Started
from .handlers.take_fee import TakeFee
from .handlers.withdrawed import Withdrawed

from .commit_processors.created_entry import CreatedEntry

commit_processors = [
    CreatedEntry()
]
schedule_processors = []

EVENTS_HANDLERS = [
    CancelDebt,
    CollateralBalance,
    ConvertPay,
    Created,
    Deposited,
    EmergencyRedeemed,
    PayOffDebt,
    Rebuy,
    Redeemed,
    SetBurner,
    SetConverter,
    SetUrl,
    Started,
    TakeFee,
    Withdrawed
]

collateral = Contract(
    "Collateral",
    EVENTS_HANDLERS,
    commit_processors,
    schedule_processors,
    contract_connection
)
