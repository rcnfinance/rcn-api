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
from .handlers.set_converter import SetConverter
from .handlers.set_url import SetUrl
from .handlers.started import Started
from .handlers.take_fee import TakeFee
from .handlers.withdrawed import Withdrawed

from .commit_processors.created import Created as CreatedCommitProcessor
from .commit_processors.deposited import Deposited as DepositedCommitProcessor
from .commit_processors.withdrawed import Withdrawed as WithdrawedCommitProcessor
from .commit_processors.started import Started as StartedCommitProcessor
from .commit_processors.redeemed import Redeemed as RedeemedCommitProcessor
from .commit_processors.emergency_redeemed import EmergencyRedeemed as EmergencyRedeemedCommitProcessor
from .commit_processors.pay_off_debt import PayOffDebt as PayOffDebtCommitProcessor
from .commit_processors.convert_pay import ConvertPay as ConvertPayCommitProcessor
from .commit_processors.rebuy import Rebuy as ReBuyCommitProcessor
from .commit_processors.cancel_debt import CancelDebt as CancelDebtCommitProcessor
from .commit_processors.take_fee import TakeFee as TakeFeeCommitProcessor
from .commit_processors.collateral_balance import CollateralBalance as CollateralBalanceCommitProcessor

commit_processors = [
    CreatedCommitProcessor(),
    DepositedCommitProcessor(),
    WithdrawedCommitProcessor(),
    StartedCommitProcessor(),
    RedeemedCommitProcessor(),
    EmergencyRedeemedCommitProcessor(),
    PayOffDebtCommitProcessor(),
    ConvertPayCommitProcessor(),
    ReBuyCommitProcessor(),
    CancelDebtCommitProcessor(),
    TakeFeeCommitProcessor(),
    CollateralBalanceCommitProcessor()
]

schedule_processors = []

event_handlers = [
    CancelDebt,
    CollateralBalance,
    ConvertPay,
    Created,
    Deposited,
    EmergencyRedeemed,
    PayOffDebt,
    Rebuy,
    Redeemed,
    SetUrl,
    Started,
    TakeFee,
    Withdrawed    
]

Collateral = Contract(
    "Collateral",
    event_handlers,
    commit_processors,
    schedule_processors,
    contract_connection
)
