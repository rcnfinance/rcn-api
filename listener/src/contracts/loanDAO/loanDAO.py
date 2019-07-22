import os
from contract import Contract
from ethereum_connection import EthereumConnection
from ethereum_connection import ContractConnection

ADDRESS = os.environ.get("LOANDAO_ADDRESS")

ABI_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "abi.json"
)
URL_NODE = os.environ.get("URL_NODE")


eth_conn = EthereumConnection(URL_NODE)
contract_connection = ContractConnection(eth_conn, ADDRESS, ABI_PATH)


from .handlers.join import Join
from .handlers.leave import Leave
from .handlers.pay_back import PayBack
from .handlers.pool_created import PoolCreated
from .handlers.pool_started import PoolStarted
from .handlers.collected import Collected

from .commit_processors.join import Join as JoinCommitProcessor
from .commit_processors.leave import Leave as LeaveCommitProcessor
from .commit_processors.pay_back import PayBack as PayBackCommitProcessor
from .commit_processors.pool_created import PoolCreated as PoolCreatedCommitProcessor
from .commit_processors.pool_started import PoolStarted as PoolStartedCommitProcessor
from .commit_processors.collected import CollectePayBackCommitProcessord as CollectedCommitProcessor


commit_processors = [
    JoinCommitProcessor(),
    LeaveCommitProcessor(),
    PayBackCommitProcessor(),
    PoolCreatedCommitProcessor(),
    PoolStartedCommitProcessor(),
    CollectedCommitProcessor()
]

schedule_processors = []

event_handlers = [
    Join,
    Leave,
    PayBack,
    PoolCreated,
    PoolStarted,
    Collected
]

Loandao = Contract(
    "Loandao",
    event_handlers,
    commit_processors,
    schedule_processors,
    contract_connection
)
