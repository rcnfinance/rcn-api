import json
import time
import web3
from web3 import Web3

class EventListener(object):
    """docstring for EventListener"""

    def __init__(self, config_filename, filter_log, handler):
        super(EventListener, self).__init__()
        self._filter = filter_log
        self._handler = handler
        self._config_filename = config_filename

        self._initialize()

    def _initialize(self):
        self._config = self._open_config()
        self._url_node = self._config['URL_NODE']
        self._contract_address = self._config['CONTRACT_ADDRESS']
        self._abi = self._config['ABI']

        self._node_provider = web3.HTTPProvider(self._url_node)
        self._w3 = Web3(self._node_provider)
        self._contract = self._w3.eth.contract(
            address=self._w3.toChecksumAddress(self._contract_address),
            abi=self._abi
        )

    def _open_config(self):
        return json.load(open(self._config_filename, 'r'))

    def _actualize_config(self):
        json.dump(self._config, open(self._config_filename, 'w'), indent=4, sort_keys=True)

    def main_loop(self, interval_sleep=10):
        while True:
            new_entries = self._filter.get_new_entries()
            print('There are {} new new_entries'.format(len(new_entries)))
            for event in new_entries:
                self._handler.handle(event)
            time.sleep(interval_sleep)