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


from .handlers.approval_for_all import ApprovalForAll
from .handlers.approval import Approval
from .handlers.cancel_debt import CancelDebt
from .handlers.collateral_balance import CollateralBalance
from .handlers.convert_pay import ConvertPay
from .handlers.created import Created
from .handlers.deposited import Deposited
from .handlers.emergency_redeemed import EmergencyRedeemed
from .handlers.ownership_transferred import OwnershipTransferred
from .handlers.pay_off_debt import PayOffDebt
from .handlers.readed_oracle import ReadedOracle
from .handlers.rebuy import Rebuy
from .handlers.redeemed import Redeemed
from .handlers.set_converter import SetConverter
from .handlers.set_max_spread_ratio import SetMaxSpreadRatio
from .handlers.set_URI_provider import SetURIProvider
from .handlers.set_url import SetUrl
from .handlers.started import Started
from .handlers.take_fee import TakeFee
from .handlers.transfer import Transfer
from .handlers.withdrawed import Withdrawed

from .commit_processors.approval_for_all import ApprovalForAll as ApprovalForAllCommitProcessor
from .commit_processors.approval import Approval as ApprovalCommitProcessor
from .commit_processors.cancel_debt import CancelDebt as CancelDebtCommitProcessor
from .commit_processors.collateral_balance import CollateralBalance as CollateralBalanceCommitProcessor
from .commit_processors.convert_pay import ConvertPay as ConvertPayCommitProcessor
from .commit_processors.created import Created as CreatedCommitProcessor
from .commit_processors.deposited import Deposited as DepositedCommitProcessor
from .commit_processors.emergency_redeemed import EmergencyRedeemed as EmergencyRedeemedCommitProcessor
from .commit_processors.ownership_transferred import OwnershipTransferred as OwnershipTransferredCommitProcessor
from .commit_processors.pay_off_debt import PayOffDebt as PayOffDebtCommitProcessor
from .commit_processors.readed_oracle import ReadedOracle as ReadedOracleCommitProcessor
from .commit_processors.rebuy import Rebuy as ReBuyCommitProcessor
from .commit_processors.redeemed import Redeemed as RedeemedCommitProcessor
from .commit_processors.set_converter import SetConverter as SetConverterCommitProcessor
from .commit_processors.set_max_spread_ratio import SetMaxSpreadRatio as SetMaxSpreadRatioCommitProcessor
from .commit_processors.set_URI_provider import SetURIProvider as SetURIProviderCommitProcessor
from .commit_processors.set_url import SetUrl as SetUrlCommitProcessor
from .commit_processors.started import Started as StartedCommitProcessor
from .commit_processors.take_fee import TakeFee as TakeFeeCommitProcessor
from .commit_processors.transfer import Transfer as TransferCommitProcessor
from .commit_processors.withdrawed import Withdrawed as WithdrawedCommitProcessor

commit_processors = [
    ApprovalForAllCommitProcessor(),
    ApprovalCommitProcessor(),
    CancelDebtCommitProcessor(),
    CollateralBalanceCommitProcessor(),
    ConvertPayCommitProcessor(),
    CreatedCommitProcessor(),
    DepositedCommitProcessor(),
    EmergencyRedeemedCommitProcessor(),
    OwnershipTransferredCommitProcessor(),
    PayOffDebtCommitProcessor(),
    ReadedOracleCommitProcessor(),
    ReBuyCommitProcessor(),
    RedeemedCommitProcessor(),
    SetConverterCommitProcessor(),
    SetMaxSpreadRatioCommitProcessor(),
    SetURIProviderCommitProcessor(),
    SetUrlCommitProcessor(),
    StartedCommitProcessor(),
    TakeFeeCommitProcessor(),
    TransferCommitProcessor(),
    WithdrawedCommitProcessor()
]

schedule_processors = []

event_handlers = [
    ApprovalForAll,
    Approval,
    CancelDebt,
    CollateralBalance,
    ConvertPay,
    Created,
    Deposited,
    EmergencyRedeemed,
    OwnershipTransferred,
    PayOffDebt,
    ReadedOracle,
    Rebuy,
    Redeemed,
    SetConverter,
    SetMaxSpreadRatio,
    SetURIProvider,
    SetUrl,
    Started,
    TakeFee,
    Transfer,
    Withdrawed
]

collateral = Contract(
    "Collateral",
    event_handlers,
    commit_processors,
    schedule_processors,
    contract_connection
)
