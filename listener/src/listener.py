import json
import time
import logging
import logging.handlers
import web3
from web3 import Web3
import db
from models import Event
from handlers import get_class_by_event

CONFIG_PATH = "config.json"


def save_event(event_to_save):
    event = Event()

    event.address = event_to_save.get('address')
    event.block_hash = event_to_save.get('blockHash').hex()
    event.block_number = event_to_save.get('blockNumber')
    event.data = event_to_save.get('data')
    event.log_index = event_to_save.get('logIndex')
    event.topics = [topic.hex() for topic in event_to_save.get('topics')]
    event.transaction_hash = event_to_save.get('transactionHash').hex()
    event.transaction_index = event_to_save.get('transactionIndex')

    event.save()
    return event

def get_last_event_saved():
    # return None or Event
    return Event.objects.order_by('-block_number').limit(1).first()

def get_numblock_to_search():
    num_block = 0
    event = get_last_event_saved()
    if event:
        num_block = event.block_number + 1
    return num_block


def get_all_events():
    return log.get_all_entries()

def get_new_entries():
    return log.get_new_entries()

def sync_db():
    logger = logging.getLogger(__name__)
    all_events = get_all_events()
    logger.info('There are {} new entries to sync'.format(len(all_events)))

    for event in all_events:
        logger.debug('Process event {}'.format(event))
        process_event(event)


def process_event(event):
    # try save document, on error delete document. sys.exit()?
    event_document = save_event(event)

    eventClass = get_class_by_event(event)
    logger.info('Event type {}'.format(type(eventClass).__name__))
    eventClass.do()

def listen(sec=5):
    logger = logging.getLogger(__name__)
    while True:
        new_entries = get_new_entries()
        logger.info('There are {} new entries'.format(len(new_entries)))

        for event in new_entries:
            logger.debug('Process event {}'.format(event))
            process_event(event)

        time.sleep(sec)

def main():
    sync_db()
    listen()

def setup_logging(level=logging.INFO):
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=level)

if __name__ == '__main__':
    setup_logging(logging.INFO)
    logger = logging.getLogger(__name__)

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

    numblock_to_search = get_numblock_to_search()
    logger.info('Creating filter from block {}'.format(numblock_to_search))

    filter_data = {
        "fromBlock": numblock_to_search,
        "toBlock": "latest",
        "address": contract.address
    }

    log = w3.eth.filter(filter_params=filter_data)
    main()