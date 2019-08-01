import os
from ethereum_connection import EthereumConnection
from ethereum_connection import ContractConnection
from models import Loan

ABI_PATH = os.path.join(
    "/project/abi",
    "rateOracle.json"
)
URL_NODE = os.environ.get("URL_NODE")

eth_conn = EthereumConnection(URL_NODE)

class OracleInterface():
    def __init__(self, contract_connection):
        self.__contract_connection = contract_connection
        self.fn = self.__contract_connection.contract.functions

    def readSample(self, data, oracle):
        contract_connection_oracle = ContractConnection(eth_conn, oracle, ABI_PATH)
        contract_oracle = contract_connection_oracle.contract.functions
        return contract_oracle.readSample(data).call()


