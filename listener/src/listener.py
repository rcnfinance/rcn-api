import json
import time
import logging
import logging.handlers
import web3

from web3 import Web3
from models import Event, Commit
from handlers import get_class_by_event
from mongoengine import connect
from utils import event_id

CONFIG_PATH = "config.json"
logger = logging.getLogger(__name__)

class Listener:
    start_sync = 3169000
    current_block = 3169000
    safe_block = 3169000
    
    def __init__(self, buffer):
        self.buffer = buffer
        self.buffer.subscribe_integrity(self.integrity_fault)

    def get_range_events(self, start, end):
        return self.w3.eth.getLogs({
            "fromBlock": start,
            "toBlock": end,
            "address": self.contract.address
        })
    
    def get_last_events(self, start):
        return self.w3.eth.getLogs({
            "fromBlock": start,
            "toBlock": 'latest',
            "address": self.contract.address
        })

    def integrity_fault(self):
        self.current_block = self.start_sync
        self.safe_block = self.start_sync

    def listen(self, sec=1):
        logger.info('Started listening')
        while True:
            # Tick to current block time
            current_block = self.w3.eth.getBlock('latest').number
            jump = min(current_block, self.safe_block + 1000)

            if jump == current_block:
                new_entries = self.get_last_events(self.safe_block)
            else:
                new_entries = self.get_range_events(self.safe_block, jump)

            logger.info('There are {} new entries {} -> {} | {}'.format(len(new_entries), self.safe_block, jump, current_block))
            self.buffer.feed(jump, new_entries)

            self.current_block = jump
            self.safe_block = int((self.safe_block + jump) / 2)

            time.sleep(sec)

    def event_time(self, event):
        return self.w3.eth.getBlock(event.get('blockNumber')).get("timestamp")

    def setup_logging(self, level=logging.INFO):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=level)

    def run(self):
        self.connection = connect(db='rcn', host='mongo')
        self.connection.drop_database('rcn')

        self.setup_logging(logging.INFO)

        config = json.load(open(CONFIG_PATH, 'r'))

        url_node = config['URL_NODE']
        contract_address = config['CONTRACT_ADDRESS']
        abi = config['ABI']

        node_provider = web3.HTTPProvider(url_node)
        w3 = Web3(node_provider)
        self.contract = w3.eth.contract(
            address=w3.toChecksumAddress(contract_address),
            abi=abi
        )

        logger.info('Creating filter from block {}'.format(0))

        self.w3 = w3
        self.listen()
