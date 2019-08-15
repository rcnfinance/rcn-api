import os
from contract import Contract
from ethereum_connection import EthereumConnection
from ethereum_connection import ContractConnection

from .oracle_factory_interface import OracleFactoryInterface

ADDRESS = os.environ.get("ORACLE_FACTORY_ADDRESS")

ABI_PATH = os.path.join(
    "/project/contracts/oracleFactory/abi",
    "OracleFactory.json"
)
URL_NODE = os.environ.get("URL_NODE")


eth_conn = EthereumConnection(URL_NODE)
contract_connection = ContractConnection(eth_conn, ADDRESS, ABI_PATH)

oracle_factory_interface = OracleFactoryInterface(contract_connection)

from .handlers.provide import Provide

from .commit_processors.provide import Provide as ProvideCommitProcessor


commit_processors = [
    ProvideCommitProcessor()
]

schedule_processors = []

event_handlers = [
    Provide,
]

Oraclefactory = Contract(
    "Oraclefactory",
    event_handlers,
    commit_processors,
    schedule_processors,
    contract_connection
)
