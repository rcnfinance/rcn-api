import os
from ethereum_connection import EthereumConnection
from ethereum_connection import ContractConnection

ADDRESS = os.environ.get("ORACLE_FACTORY_ADDRESS")

ABI_PATH = os.path.join(
    "/project/contracts/oracleFactory/abi",
    "OracleFactory.json"
)
URL_NODE = os.environ.get("URL_NODE")


eth_conn = EthereumConnection(URL_NODE)
contract_connection = ContractConnection(eth_conn, ADDRESS, ABI_PATH)

class OracleFactoryInterface():
    def __init__(self, contract_connection):
        self.__contract_connection = contract_connection
        self.fn = self.__contract_connection.contract.functions

    def get_symbol(self, _oracle):
        try:
            return self.fn.oracleToSymbol(_oracle).call()
        except Exception:
            return '0x0'
