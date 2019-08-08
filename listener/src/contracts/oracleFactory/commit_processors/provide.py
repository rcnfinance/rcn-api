from models import OracleRate
from contracts.commit_processor import CommitProcessor
import requests

class Provide(CommitProcessor):
    def __init__(self):
        self.opcode = "provide_oracleFactory"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        oracleRate = OracleRate()

        oracleRate.oracle = data.get("oracle")
        oracleRate.signer = data.get("signer")
        oracleRate.rate = data.get("rate")

        # defining the api-endpoint  
        API_ENDPOINT = "https://discordapp.com/api/webhooks/609025990974505000/FiC9Q5JpAfTmb35kCeHhHqwb7fCcCtg9bPv5eq73XDNPHSsPaL1ymhV4kzAcTCgRsHFy"

        separation = '-----' + '\n' 
        title = 'New Rate Provided:' + '\n' 
        oracle = 'Oracle: ' + oracleRate.oracle + '\n'
        signer = 'Signer:' + oracleRate.signer + '\n'
        rate = 'Rate:' + oracleRate.rate + '\n'  

        rateProvided = separation + title + oracle + signer + rate + separation         

        # data to be sent to api 
        payload = {'username':'Test', 
                    'content': rateProvided } 
        
        # sending post request and saving response as response object 
        r = requests.post(url = API_ENDPOINT, data = payload) 
        
        # extracting response text  
        oracle_url = r.text 
        print("The oracle URL is:%s"%oracle_url) 

        commit.save()
        oracleRate.save()