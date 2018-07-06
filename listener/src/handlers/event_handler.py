import logging
import json
import web3


CONFIG_PATH = "config.json"

class EventHandler():
    def __init__(self, event):
        self._event = event
        self._parse()
        self._logger = logging.getLogger(__name__)

        config = json.load(open(CONFIG_PATH, 'r'))

        url_node = config['URL_NODE']
        contract_address = config['CONTRACT_ADDRESS']
        abi = config['ABI']

        node_provider = web3.HTTPProvider(url_node)
        self._w3 = web3.Web3(node_provider)
        self._contract = self._w3.eth.contract(
            address=self._w3.toChecksumAddress(contract_address),
            abi=abi
        )

    def _parse(self):
        raise NotImplementedError()