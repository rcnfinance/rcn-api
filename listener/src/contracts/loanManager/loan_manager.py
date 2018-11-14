import os
from contract import Contract
from ethereum_connection import EthereumConnection
from ethereum_connection import ContractConnection

from .loan_manager_interface import LoanManagerInteface

from .handlers.approved import Approved
from .handlers.approved_error import ApprovedError
from .handlers.approved_rejected import ApprovedRejected
from .handlers.canceled import Canceled
from .handlers.cosigned import Cosigned
from .handlers.lent import Lent
from .handlers.readed_oracle import ReadedOracle
from .handlers.requested import Requested
from .handlers.settled_cancel import SettledCancel
from .handlers.settled_lend import SettledLend

from .commit_processors.approved import Approved as ApprovedCommitProcessor
from .commit_processors.canceled import Canceled as CanceledCommitProcessor
from .commit_processors.cosigned import Cosigned as CosignedCommitProcessor
from .commit_processors.lent import Lent as LentCommitProcessor
from .commit_processors.requested import Requested as RequestedCommitProcessor

ADDRESS = "0xA6E4B95A0D1be10E886317Fe711a4515544c578a"

ABI_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "abi.json"
)
URL_NODE = "https://ropsten.node.rcn.loans:8545/"

eth_conn = EthereumConnection(URL_NODE)
contract_connection = ContractConnection(eth_conn, ADDRESS, ABI_PATH)

debt_engine_interface = LoanManagerInteface(contract_connection)


commit_processors = [
    ApprovedCommitProcessor(),
    CanceledCommitProcessor(),
    CosignedCommitProcessor(),
    LentCommitProcessor(),
    RequestedCommitProcessor()
]

schedule_processors = []

event_handlers = [
    Approved,
    ApprovedError,
    ApprovedRejected,
    Canceled,
    Cosigned,
    Lent,
    ReadedOracle,
    Requested,
    SettledCancel,
    SettledLend
]

loan_manager = Contract(
    "LoanManager",
    event_handlers,
    commit_processors,
    schedule_processors,
    contract_connection
)
