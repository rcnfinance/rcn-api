import os
import logging
import json
import web3


logger = logging.getLogger(__name__)


class AddressNotFound(Exception):
    pass


class AddressExist(Exception):
    pass


class Contract:
    def __init__(self, name, address, abi_path, event_handlers, commit_processors, schedule_processors):
        self.name = name
        self.address = [address]
        self.abi_path = abi_path
        self.event_handlers = event_handlers
        self.commit_processors = commit_processors
        self.schedule_processors = schedule_processors

        self.__url_node = os.environ.get("URL_NODE")

        self.__init_struct_event_handlers()
        self.__init_struct_commit_processors()
        self.__init_struct_schedule_processors()

    def __init_struct_event_handlers(self):
        self.__struct_event_handlers = {
            handler.signature_hash: handler for handler in self.event_handlers
        }

    def get_handler_by_signature(self, signature):
        logger.info("signature: {}".format(signature))
        logger.info("struct handlers: {}".format(self.__struct_event_handlers))
        handler = self.__struct_event_handlers.get(signature)
        return handler

    def __init_struct_commit_processors(self):
        self.__struct_commit_processors = {
            cp.opcode: cp for cp in self.commit_processors
        }

    def get_commit_processor_by_opcode(self, opcode):
        commit_processor = self.__struct_commit_processors.get(opcode)
        return commit_processor

    def get_opcodes_commit_processors(self):
        return self.__struct_commit_processors.keys()

    def __init_struct_schedule_processors(self):
        self.__struct_schedule_processors = {
            sp.opcode: sp for sp in self.schedule_processors
        }

    def get_schedule_processor_by_opcode(self, opcode):
        schedule_processor = self.__struct_schedule_processors.get(opcode)
        return schedule_processor

    def __get_node_provider(self):
        provider = getattr(self, "__w3_provider", None)
        if provider is None:
            provider = web3.HTTPProvider(self.__url_node)
            setattr(self, "__w3_provider", provider)
        return provider

    def __get_w3(self):
        w3 = getattr(self, "__w3", None)
        if w3 is None:
            w3 = web3.Web3(self.__get_node_provider())
            setattr(self, "__w3", w3)
        return w3

    def get_w3_contract(self, address):
        if address in self.address:
            w3 = self.__get_w3()
            checksum_address = w3.toChecksumAddress(address)
            contract = w3.eth.contract(
                address=checksum_address,
                abi=json.load(open(self.abi_path, "r"))
            )
            return contract
        else:
            raise AddressNotFound()

    def add_address(self, address):
        if address not in self.address:
            self.address.append(address)
        else:
            raise AddressExist()

    def handle_event(self, log):
        event_hash = log.get("topic0")
        logger.info("log.address: {}, log.topic0:{}".format(log.get("address"), log.get("topics")[0]))
        handler = self.get_handler_by_signature(event_hash)
        h = handler(self.get_w3_contract(log.address), log)
        logger.info("Handler name: {}".format(h.name()))
        commits = h.handle()
        return commits

    def handle_commit(self, commit, optional_data={}):
        commit_processor = self.get_commit_processor_by_opcode(commit.opcode)
        logger.info("commit class {}".format(commit_processor.name))
        commit_processor.process(commit, **optional_data)

    def rollback_commit(self, commit, optional_data={}):
        commit_processor = self.get_commit_processor_by_opcode(commit.opcode)
        logger.info("commit class {}".format(commit_processor.name))
        commit_processor.apply_old(commit, **optional_data)

    def handle_schedule(self, schedule, optional_data={}):
        schedule_processor = self.get_schedule_processor_by_opcode(schedule.opcode)
        return schedule_processor.process(schedule, **optional_data)


# class Contract():
#     def __init__(self, name, event_handlers, commit_processors, schedule_processors, contract_connection):
#         self._name = name
#         self._address = contract_connection.address
#         self._contract_connection = contract_connection
#         self._event_handlers = event_handlers
#         self._commit_processors = commit_processors
#         self._schedule_processors = schedule_processors
#         self.__handlers()
#         self.__commit_processors()
#         self.__schedule_processors()
#         self._logger = logging.getLogger(__name__)

#     def __commit_processors(self):
#         self._commit_processors = {commit_processor.opcode: commit_processor for commit_processor in self._commit_processors}

#     def __schedule_processors(self):
#         self._schedule_processors = {schedule_processor.opcode: schedule_processor for schedule_processor in self._schedule_processors}

#     def __handlers(self):
#         self._handlers = {handler.signature_hash: handler for handler in self._event_handlers}
    
#     def is_my_event(self, event):
#         event_hash = event.get("topic0")
#         event_address = event.get("address")
#         if event_hash in self._handlers and event_address == self._address:
#             return True
#         else:
#             return False

#     def handle_event(self, event):
#         event_hash = event.get("topic0")
#         handler = self._handlers.get(event_hash)
#         self._logger.info("Handler name: {}".format(handler.__name__))
#         h = handler(self._contract_connection, event)
#         return h

