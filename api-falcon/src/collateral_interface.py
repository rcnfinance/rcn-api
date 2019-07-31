import os
from ethereum_connection import EthereumConnection
from ethereum_connection import ContractConnection
import requests 
from models import Collateral, Loan
from oracle_interface import oracle_interface
import logging
import requests

COLLATERAL_ADDRESS = os.environ.get("COLLATERAL_ADDRESS")

ABI_PATH = os.path.join(
    "/project/abi",
    "collateral.json"
)
URL_NODE = os.environ.get("URL_NODE")

ORACLE_URL = "https://oracle.ripio.com/rate"

eth_conn = EthereumConnection(URL_NODE)
logger = logging.getLogger(__name__)

class CollateralInterface():
    def __init__(self, contract_connection):
        self.__contract_connection = contract_connection
        self.fn = self.__contract_connection.contract.functions

    def get_collateral_ratio(self, id):
        (tokens, equivalent) = self.get_oracle_data(id)
        return self.fn.collateralRatio(id, tokens, equivalent).call()

    def get_liquidation_delta_ratio(self, _id):
        (tokens, equivalent) = self.get_oracle_data(id)
        return self.fn.liquidationDeltaRatio(id, tokens, equivalent).call()

    def get_loan_manager_token(self):
        return self.fn.loanManager()

    def get_oracle_data(self, id):
        try:
            collateral = Collateral.objects.get(id=str(id))
          
            debtId = collateral.debtId
            loan = Loan.objects.get(id=debtId)

            oracle = loan.oracle

            response = requests.get(url = ORACLE_URL)
            oracleData = response.json() 
            print('OracleData:', oracleData)
            currencyObject = [x for x in oracleData if x.currency == loan.currency]
            print('currency Object:', currencyObject)
            if(currencyObject.length > 0):
                dataCurrency = currencyObject[0].data
                (_tokens,_equivalent) = oracle_interface.readSample(dataCurrency, oracle)    
            else: 
                _tokens = 0
                _equivalent = 0
        

            return (_tokens,_equivalent)
        except Collateral.DoesNotExist:
            logger.warning("Collateral with id {} does not exist".format(str(id)))


