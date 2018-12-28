import logging


class EventHandler():
    def __init__(self, contract_conn, event):
        self._event = event
        self._contract_conn = contract_conn
        self._logger = logging.getLogger(self.__class__.__name__)
        self._event_abi = self._contract_conn.abi
        self._parse()

    def _parse(self):
        raise NotImplementedError()

    def handle(self):
        raise NotImplementedError()

    def _block_timestamp(self):
        return self._contract_conn.w3.eth.getBlock(self._block_number).timestamp

# def get_abi_event(abi, signature):
#     for abi_event in abi.events:
#         if signature.name == abi_event.name
#         return abi_event