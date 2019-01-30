import os
import time
import logging
import logging.handlers
from raven.handlers.logging import SentryHandler
from raven.conf import setup_logging


logger = logging.getLogger(__name__)


class Listener:
    def __init__(self, buffer, contract_manager):
        self.buffer = buffer
        self.buffer.subscribe_integrity(self.integrity_fault)
        self._contract_manager = contract_manager
        self.setup_logging(logging.INFO)

    def get_range_events(self, start, end):
        logger.info("Getting events in range {} to {}".format(start, end))
        contract_addresses = [contract._address for contract in self._contract_manager._contracts]
        logs = self._contract_manager._ethereum_connection.w3.eth.getLogs({
            "fromBlock": start,
            "toBlock": end,
            "address": contract_addresses
        })
        return logs

    def get_last_events(self, start):
        logger.info("Getting events in range {} to latest".format(start))
        contract_addresses = [contract._address for contract in self._contract_manager._contracts]
        logs = self._contract_manager._ethereum_connection.w3.eth.getLogs({
            "fromBlock": start,
            "toBlock": 'latest',
            "address": contract_addresses
        })
        return logs

    def integrity_fault(self):
        self.current_block = self.start_sync
        self.safe_block = self.start_sync

    def listen(self, sec=1):
        logger.info('Started listening')
        while True:
            # Tick to current block time
            last_block = self._contract_manager._ethereum_connection.w3.eth.getBlock('latest')
            dest_number = min(last_block.number, self.safe_block + 5000)

            if dest_number == last_block.number:
                dest_timestamp = last_block.timestamp
                new_entries = self.get_last_events(self.safe_block)
            else:
                dest_timestamp = self._contract_manager._ethereum_connection.w3.eth.getBlock(dest_number).timestamp
                new_entries = self.get_range_events(self.safe_block, dest_number)

            message = 'There are {} new entries {} -> {} | {}'.format(
                len(new_entries), self.safe_block, dest_number, last_block.number
            )
            logger.info(message)

            self.buffer.feed(dest_number, dest_timestamp, new_entries)

            self.current_block = dest_number
            self.safe_block = int((self.safe_block + dest_number) / 2)

            if dest_number == last_block.number:
                time.sleep(sec)

    def setup_logging(self, level=logging.INFO):
        handler = SentryHandler(os.environ.get("SENTRY_DSN"))
        handler.setLevel(logging.ERROR)
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=level)
        setup_logging(handler)

    def run(self):
        self.start_sync = int(os.environ['START_SYNC'])
        self.current_block = self.start_sync
        self.safe_block = self.start_sync

        logger.info('Creating filter from block {}'.format(0))

        # self.w3 = SafeWeb3(w3)
        self.listen()
