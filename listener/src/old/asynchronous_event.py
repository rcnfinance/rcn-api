import web3
from web3 import Web3
import json
from web3.auto import w3
import asyncio


def handle_event(event):
    print(event)

async def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        await asyncio.sleep(poll_interval)

def main():
    block_filter = w3.eth.filter('latest')
    tx_filter = w3.eth.filter('pending')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(block_filter, 2),
                log_loop(tx_filter, 2)))
    finally:
        loop.close()

if __name__ == '__main__':
    URL_NODE_ROPSTEN = 'https://ropsten.infura.io/'
    LOCAL_NODE_ROPSTEN = 'https://172.31.24.238:8545'
    DEV_NODE_ROPSTEN = 'http://ec2-18-221-133-10.us-east-2.compute.amazonaws.com:8545'
    CONTRACT_ADDRESS = '0xbee217bfe06c6faaa2d5f2e06ebb84c5fb70d9bf'
    ABI_FILEPATH  = 'abi.json'

    ropsten_provider = web3.HTTPProvider(DEV_NODE_ROPSTEN)
    w3 = Web3(ropsten_provider)
    contract = w3.eth.contract(
        address=w3.toChecksumAddress(CONTRACT_ADDRESS),
        abi=json.load(open(ABI_FILEPATH))
    )
    main()