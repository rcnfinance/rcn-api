import logging


class EventHandler():
    def __init__(self, contract_conn, event):
        self._event = event
        self._contract_conn = contract_conn
        self._logger = logging.getLogger(self.__class__.__name__)
        self._parse()

    def _parse(self):
        raise NotImplementedError()

    def handle(self):
        raise NotImplementedError()

    def _block_timestamp(self):
        return self._contract_conn.w3.eth.getBlock(self._block_number).timestamp