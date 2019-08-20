import logging
import web3


class EventHandler():
    def __init__(self, w3_contract, event):
        self._event = event
        self._event_name = self.signature.split("(")[0]
        self._w3_contract = w3_contract
        self._logger = logging.getLogger(self.__class__.__name__)
        self._parse_args()
        self._normalize()
        self._tx = self._get_transaction()

    def _parse_args(self):
        self._logger.info("event: {}".format(self._event))

        self._event_abi = web3.utils.abi.filter_by_name(self._event_name, self._w3_contract.abi)[0]
        self._args = dict(web3.utils.events.get_event_data(self._event_abi, self._event).args)
        self._block_number = str(self._event.get('blockNumber'))
        self._transaction = self._event.get('transactionHash').hex()

    def _normalize(self):
        pass

    def handle(self):
        raise NotImplementedError()

    def _block_timestamp(self):
        return self._w3_contract.web3.eth.getBlock(int(self._block_number)).timestamp

    def _get_transaction(self):
        return self._w3_contract.web3.eth.getTransaction(self._transaction)

    def name(self):
        return self._event_name
