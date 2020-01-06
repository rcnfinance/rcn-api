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
from .handlers.claimed_expired import ClaimedExpired
from .handlers.claimed_liquidation import ClaimedLiquidation
from .handlers.closed_auction import ClosedAuction
from .handlers.created import Created
from .handlers.deposited import Deposited
from .handlers.emergency_redeemed import EmergencyRedeemed
from .handlers.ownership_transferred import OwnershipTransferred
from .handlers.redeemed import Redeemed
from .handlers.set_URI_provider import SetURIProvider
from .handlers.set_url import SetUrl
from .handlers.started import Started
from .handlers.transfer import Transfer
from .handlers.withdraw import Withdraw

from .commit_processors.approval_for_all import ApprovalForAll as ApprovalForAllCommitProcessor
from .commit_processors.approval import Approval as ApprovalCommitProcessor
from .commit_processors.claimed_expired import ClaimedExpired as ClaimedExpiredCommitProcessor
from .commit_processors.claimed_liquidation import ClaimedLiquidation as ClaimedLiquidationCommitProcessor
from .commit_processors.closed_auction import ClosedAuction as ClosedAuctionCommitProcessor
from .commit_processors.created import Created as CreatedCommitProcessor
from .commit_processors.deposited import Deposited as DepositedCommitProcessor
from .commit_processors.emergency_redeemed import EmergencyRedeemed as EmergencyRedeemedCommitProcessor
from .commit_processors.ownership_transferred import OwnershipTransferred as OwnershipTransferredCommitProcessor
from .commit_processors.redeemed import Redeemed as RedeemedCommitProcessor
from .commit_processors.set_URI_provider import SetURIProvider as SetURIProviderCommitProcessor
from .commit_processors.set_url import SetUrl as SetUrlCommitProcessor
from .commit_processors.started import Started as StartedCommitProcessor
from .commit_processors.transfer import Transfer as TransferCommitProcessor
from .commit_processors.withdraw import Withdraw as WithdrawCommitProcessor

commit_processors = [
    ApprovalForAllCommitProcessor(),
    ApprovalCommitProcessor(),
    ClaimedExpiredCommitProcessor(),
    ClaimedLiquidationCommitProcessor(),
    ClosedAuctionCommitProcessor(),
    CreatedCommitProcessor(),
    DepositedCommitProcessor(),
    EmergencyRedeemedCommitProcessor(),
    OwnershipTransferredCommitProcessor(),
    RedeemedCommitProcessor(),
    SetURIProviderCommitProcessor(),
    SetUrlCommitProcessor(),
    StartedCommitProcessor(),
    TransferCommitProcessor(),
    WithdrawCommitProcessor()
]

schedule_processors = []

event_handlers = [
    ApprovalForAll,
    Approval,
    ClaimedExpired,
    ClaimedLiquidation,
    ClosedAuction,
    Created,
    Deposited,
    EmergencyRedeemed,
    OwnershipTransferred,
    Redeemed,
    SetURIProvider,
    SetUrl,
    Started,
    Transfer,
    Withdraw
]

collateral = Contract(
    "Collateral",
    event_handlers,
    commit_processors,
    schedule_processors,
    contract_connection
)
