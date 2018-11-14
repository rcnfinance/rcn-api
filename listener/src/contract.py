import logging

class Contract():
    def __init__(self, name, event_handlers, commit_processors, schedule_processors, contract_connection):
        self._name = name
        self._address = contract_connection.address
        self._contract_connection = contract_connection
        self._event_handlers = event_handlers
        self._commit_processors = commit_processors
        self._schedule_processors = schedule_processors
        self.__handlers()
        self.__commit_processors()
        self.__schedule_processors()
        self._logger = logging.getLogger(__name__)

    def __commit_processors(self):
        self._commit_processors = {commit_processor.opcode: commit_processor for commit_processor in self._commit_processors}

    def __schedule_processors(self):
        self._schedule_processors = {schedule_processor.opcode: schedule_processor for schedule_processor in self._schedule_processors}

    def __handlers(self):
        self._handlers = {handler.signature_hash: handler for handler in self._event_handlers}
    
    def is_my_event(self, event):
        event_hash = event.get("topics")[0].hex()
        event_address = event.get("address")
        if event_hash in self._handlers and event_address == self._address:
            return True
        else:
            return False

    def handle_event(self, event):
        event_hash = event.get("topics")[0].hex()
        handler = self._handlers.get(event_hash)
        self._logger.info("Handler name: {}".format(handler.__name__))
        h = handler(self._contract_connection, event)
        return h

