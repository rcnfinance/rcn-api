import json
import web3
from web3 import Web3

class Handler(object):
    def __init__(self, config_filename, preservers):
        self.__init_environment(config_filename)
        self._preservers = preservers

    def __init_environment(self, config_filename):
        self._config = self._open_config(config_filename)

        self._url_node = self._config['URL_NODE']
        self._contract_address = self._config['CONTRACT_ADDRESS']
        self._abi = self._config['ABI']

        self._node_provider = web3.HTTPProvider(self._url_node)
        self._w3 = Web3(self._node_provider)
        self._contract = self._w3.eth.contract(
            address=self._w3.toChecksumAddress(self._contract_address),
            abi=self._abi
        )

    def _open_config(self, config_filepath):
        return json.load(open(config_filepath, 'r'))

    def handle(self, event):
        parsed_event = self._parse_event(event)
        self._save(parsed_event)

    def _parse_event(self, event):
        raise NotImplementedError()

    def _save(self, parsed_event):
        for preserver in self._preservers:
            preserver.preserve(parsed_event)