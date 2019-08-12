from models import OracleRate
from contracts.commit_processor import CommitProcessor
import requests
import os
from contracts.oracleFactory.oracleFactory import oracle_factory_interface
import web3

API_ENDPOINT = os.environ.get("DISCORD_WEBHOOK")
API_KEY = os.environ.get("WEBHOOK_KEY")

class Provide(CommitProcessor):
    def __init__(self):
        self.opcode = "provide_oracleFactory"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        oracleRate = OracleRate()

        oracleRate.oracle = data.get("oracle")
        oracleRate.signer = data.get("signer")
        oracleRate.raw_rate = data.get("rate")

        get_symbol = oracle_factory_interface.get_symbol(oracleRate.oracle)
        rate_decimals = int(oracleRate.raw_rate) / (10 ** 18)

        separation = '-----' + '\n' 
        title = 'New Rate Provided: ' + get_symbol + '/RCN' + '\n' 
        oracle = 'Oracle: ' + oracleRate.oracle + '\n'
        signer = 'Signer:' + oracleRate.signer + '\n'
        raw_rate = 'Raw Rate:' + oracleRate.raw_rate + '\n'  
        rate = 'Rate:' + str("{:.10f}".format(rate_decimals)) + '\n'      
        symbol = 'Symbol: ' + get_symbol + '\n'    

        rate_provided_data = separation + title + oracle + signer + rate + raw_rate + symbol + separation      
   
        # data to be sent to api 
        payload = {'username':'Test', 
                    'content': rate_provided_data } 
        
        try:
            # sending post request and saving response as response object 
            requests.post(url = API_ENDPOINT + API_KEY, data = payload) 
        except Exception:
            pass
  
        oracleRate.rate = str("{:.10f}".format(rate_decimals))
        oracleRate.symbol = get_symbol
        oracleRate.timestamp = str(commit.timestamp)

        commit.save()
        oracleRate.save()

        