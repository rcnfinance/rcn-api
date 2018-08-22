import os
import logging
import json
import web3

ABI_PATH = "engine-abi.json"

class EventHandler():
    def __init__(self, event):
        self._event = event
        self._parse()
        self._logger = logging.getLogger(self.__class__.__name__)

        url_node = os.environ['URL_NODE']
        contract_address = os.environ['CONTRACT_ADDRESS']
        abi = json.load(open(ABI_PATH, 'r'))

        node_provider = web3.HTTPProvider(url_node)
        self._w3 = web3.Web3(node_provider)
        self._contract = self._w3.eth.contract(
            address=self._w3.toChecksumAddress(contract_address),
            abi=abi
        )

    def _parse(self):
        raise NotImplementedError()

    def do(self):
        raise NotImplementedError()