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


# from .handlers.approved import Approved

# from .commit_processors.approved import Approved as ApprovedCommitProcessor


commit_processors = [
    # ApprovedCommitProcessor()
]

schedule_processors = []

event_handlers = [
    # Approved,
]

Collateral = Contract(
    "Collateral",
    event_handlers,
    commit_processors,
    schedule_processors,
    contract_connection
)
