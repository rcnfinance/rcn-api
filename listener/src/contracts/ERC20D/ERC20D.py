import os
from contract import Contract
from ethereum_connection import EthereumConnection
from ethereum_connection import ContractConnection

ADDRESS = os.environ.get("ERC20D_ADDRESS")

ABI_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "abi.json"
)
URL_NODE = os.environ.get("URL_NODE")


eth_conn = EthereumConnection(URL_NODE)
contract_connection = ContractConnection(eth_conn, ADDRESS, ABI_PATH)


from .handlers.claimed import Claimed
from .handlers.claimed_transfer import ClaimedTransfer
from .handlers.paid import Paid


from .commit_processors.claimed import Claimed as ClaimedCommitProcessor
from .commit_processors.claimed_transfer import ClaimedTransfer as ClaimedTransferCommitProcessor
from .commit_processors.paid import Paid as PaidCommitProcessor


commit_processors = [
    ClaimedCommitProcessor(),
    ClaimedTransferCommitProcessor(),
    PaidCommitProcessor()
]

schedule_processors = []

event_handlers = [
    Claimed,
    ClaimedTransfer,
    Paid
]

Erc20D = Contract(
    "Erc20D",
    event_handlers,
    commit_processors,
    schedule_processors,
    contract_connection
)
