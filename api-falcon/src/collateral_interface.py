import os
import logging
from ethereum_connection import EthereumConnection
from ethereum_connection import ContractConnection
from models import Collateral, Loan
from utils import get_oracle_data

class CollateralInterface():
    def __init__(self, contract_connection):
        self.__contract_connection = contract_connection
        self.fn = self.__contract_connection.contract.functions

    def get_collateral_ratio(self, id):
        tokens, equivalent = get_oracle_data(id)
        collateralRatio = self.fn.collateralRatio(int(id), int(tokens), int(equivalent)).call()
        print('Answer Collateral Ratio:', collateralRatio)
        return str(collateralRatio)

    def get_liquidation_delta_ratio(self, id):
        (tokens, equivalent) = get_oracle_data(id)
        return self.fn.liquidationDeltaRatio(int(id), tokens, equivalent).call()





