import json
import time
import logging
import logging.handlers
import web3
from web3 import Web3
from models import Event
from handlers import get_class_by_event
from mongoengine import connect
from utils import event_id

CONFIG_PATH = "config.json"
logger = logging.getLogger(__name__)

class Listener:
    def save_event(self, event_to_save):
        event = Event()
        event.uuid = event_id(event_to_save)
        event.save()
        return event

    def event_exist(self, event):
        return Event.objects(uuid=event_id(event)).first() != None

    def get_all_events(self):
        return self.log.get_all_entries()

    def get_new_entries(self):
        return self.log.get_new_entries()

    def sync_db(self):
        all_events = self.get_all_events()
        
        logger.info('There are {} new entries to sync'.format(len(all_events)))

        for event in all_events:
            logger.debug('Process event {}'.format(event))
            self.process_event(event)


    def process_event(self, event):
        if not self.event_exist(event):
            eventClass = get_class_by_event(event)
            logger.info('Apply event {}'.format(type(eventClass).__name__))
            eventClass.do()
            self.save_event(event)
        else:
            logger.info('Event already applied')

    def listen(self, sec=5):
        while True:
            new_entries = self.get_new_entries()
            logger.info('There are {} new entries'.format(len(new_entries)))

            for event in new_entries:
                logger.debug('Process event {}'.format(event))
                self.process_event(event)

            time.sleep(sec)

    def main(self):
        self.sync_db()
        self.listen()

    def setup_logging(self, level=logging.INFO):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=level)

    def run(self):
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

        logger.info('Creating filter from block {}'.format(0))

        filter_data = {
            "fromBlock": 0,
            "toBlock": "latest",
            "address": contract.address
        }

        self.log = w3.eth.filter(filter_params=filter_data)
        self.main()

if __name__ == '__main__':
    Listener().run()