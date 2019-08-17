from models import OracleRate
from contracts.commit_processor import CommitProcessor
import requests
import os
from contracts.oracleFactory.oracleFactory import oracle_factory_interface
import web3
from datetime import datetime
from ethereum_connection import EthereumConnection
from ethereum_connection import ContractConnection

API_ENDPOINT = os.environ.get("DISCORD_WEBHOOK")
API_KEY = os.environ.get("WEBHOOK_KEY")

ABI_PATH = os.path.join(
    "/project/contracts/oracleFactory/abi",
    "MultiSourceOracle.json"
)
URL_NODE = os.environ.get("URL_NODE")

eth_conn = EthereumConnection(URL_NODE)

class Provide(CommitProcessor):
    def __init__(self):
        self.opcode = "provide_oracleFactory"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        oracleRate = OracleRate()

        oracleRate.oracle = data.get("oracle")
        oracleRate.signer = data.get("signer")
        oracleRate.raw_rate = data.get("rate")

        contract_connection_oracle = ContractConnection(eth_conn, oracleRate.oracle, ABI_PATH)
        contract_oracle = contract_connection_oracle.contract.functions

        read_sample = contract_oracle.readSample().call()
        signer_name = contract_oracle.nameOfSigner(oracleRate.signer).call()
        median_rate = read_sample[1]
        median_rate_decimals = int(median_rate) / (10 ** 18)

        get_symbol = oracle_factory_interface.get_symbol(oracleRate.oracle)
        rate_decimals = int(oracleRate.raw_rate) / (10 ** 18)

        separation = '-----' + '\n' 
        title = 'New Rate Provided: ' + get_symbol + '/RCN' + '\n' 
        oracle = 'Oracle: ' + oracleRate.oracle + '\n'
        signer = 'Signer:' + oracleRate.signer + '\n'
        signer = 'Signer Name: ' + signer_name  + '\n' 
        raw_rate = 'Raw Rate:' + oracleRate.raw_rate + '\n'  
        rate = 'Rate:' + str("{:.10f}".format(rate_decimals)) + '\n'      
        symbol = 'Symbol: ' + get_symbol + '\n'    
        timestamp = 'Timestamp: ' + str(commit.timestamp) + '\n'  
        time_bson = 'Time Bson:' +  str(datetime.fromtimestamp(commit.timestamp)) + '\n' 
        median = 'Median Rate: ' +  str("{:.10f}".format(median_rate_decimals)) + '\n'      

        rate_provided_data = separation + title + oracle + signer + rate + raw_rate + symbol + time_bson + timestamp + median + separation      
   
        # data to be sent to api 
        payload = {'username':'Test', 
                    'content': rate_provided_data } 
        
        try:
            # sending post request and saving response as response object 
            requests.post(url = API_ENDPOINT + API_KEY, data = payload) 
        except Exception:
            pass

        oracleRate.signer_name = signer_name
        oracleRate.rate = str("{:.10f}".format(rate_decimals))
        oracleRate.median_rate = str("{:.10f}".format(median_rate_decimals))
        oracleRate.symbol = get_symbol
        oracleRate.timestamp = str(commit.timestamp)
        oracleRate.time_bson = datetime.fromtimestamp(commit.timestamp)
    
        commit.save()
        oracleRate.save()

        