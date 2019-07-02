import logging
import web3


class EventHandler():
    def __init__(self, contract_conn, event):
        self._event = event
        self._event_name = self.signature.split("(")[0]
        self._contract_conn = contract_conn
        self._logger = logging.getLogger(self.__class__.__name__)
        self._contract_abi = self._contract_conn.abi
        self._parse()
        self._normalize()
        self._tx = self._get_transaction()

    def _parse(self):
        self._logger.info("event: {}".format(self._event))

        self._event_abi = web3.utils.abi.filter_by_name(self._event_name, self._contract_abi)[0]
        self._args = dict(web3.utils.events.get_event_data(self._event_abi, self._event).args)
        self._block_number = self._event.get('blockNumber')
        self._transaction = self._event.get('transactionHash').hex()
        self._address = self._event.get('address')

    def _normalize(self):
        pass

    def handle(self):
        raise NotImplementedError()

    def _block_timestamp(self):
        return self._contract_conn.w3.eth.getBlock(self._block_number).timestamp

    def _get_transaction(self):
        return self._contract_conn.w3.eth.getTransaction(self._transaction)
