import os
from ethereum_connection import EthereumConnection
from ethereum_connection import ContractConnection

COLLATERAL_ADDRESS = os.environ.get("COLLATERAL_ADDRESS")

ABI_PATH = os.path.join(
    "/project/abi",
    "collateral.json"
)
URL_NODE = os.environ.get("URL_NODE")

eth_conn = EthereumConnection(URL_NODE)


class CollateralInterface():
    def __init__(self, contract_connection):
        self.__contract_connection = contract_connection
        self.fn = self.__contract_connection.contract.functions

    def get_collateral_ratio(self, _id,_rateTokens,_rateEquivalent):
        return self.fn.collateralRatio(_id,_rateTokens,_rateEquivalent).call()

    def get_liquidation_delta_ratio(self, _id,_rateTokens,_rateEquivalent):
        return self.fn.getCurrency(_id,_rateTokens,_rateEquivalent).call()

