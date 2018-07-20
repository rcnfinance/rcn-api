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
from processor import Processor

CONFIG_PATH = "config.json"
logger = logging.getLogger(__name__)

class Listener:
    def save_event(self, event_to_save):
        event = Event()
        event.uuid = event_id(event_to_save)
        event.save()
        return event

    def event_exist(self, event):
        return Event.objects(uuid=event_id(event)).first() is not None

    def get_all_events(self):
        return self.log.get_all_entries()

    def get_new_entries(self):
        return self.log.get_new_entries()

    def sync_db(self):
        all_events = self.get_all_events()
        
        logger.info('There are {} new entries to sync'.format(len(all_events)))

        for event in all_events:
            self.process_event(event)

    def process_event(self, event):
        logger.debug('Process event {}'.format(event))
        if not self.event_exist(event):
            eventClass = get_class_by_event(event)
            logger.info('Apply event {}'.format(type(eventClass).__name__))
            commits = eventClass.do()

            if commits:
                self.processor.execute(commits)
            self.save_event(event)
        else:
            logger.info('Event already applied')

    def listen(self, sec=1):
        while True:
            # Tick to current block time
            new_entries = self.get_new_entries()
            logger.info('There are {} new entries'.format(len(new_entries)))

            for event in new_entries:
                self.process_event(event)

            block_time = self.w3.eth.getBlock('latest').get("timestamp")
            if block_time > self.processor.clock:
                self.processor._advance_time(block_time)

            time.sleep(sec)

    def event_time(self, event):
        return self.w3.eth.getBlock(event.get('blockNumber')).get("timestamp")

    def main(self):
        self.sync_db()
        self.listen()

    def setup_logging(self, level=logging.INFO):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=level)

    def run(self):
        self.processor = Processor()

        self.connection = connect(db='rcn', host='mongo')
        self.setup_logging(logging.INFO)

        config = json.load(open(CONFIG_PATH, 'r'))

        url_node = config['URL_NODE']
        contract_address = config['CONTRACT_ADDRESS']
        abi = config['ABI']

        node_provider = web3.HTTPProvider(url_node)
        w3 = Web3(node_provider)
        contract = w3.eth.contract(
            address=w3.toChecksumAddress(contract_address),
            abi=abi
        )

        self.w3 = w3

        logger.info('Creating filter from block {}'.format(0))

        filter_data = {
            "fromBlock": 0,
            "toBlock": "latest",
            "address": contract.address
        }

        self.log = self.w3.eth.filter(filter_params=filter_data)
        self.main()

if __name__ == '__main__':
    Listener().run()