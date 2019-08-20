import logging


logger = logging.getLogger(__name__)


class ContractNotFound(Exception):
    pass


class ContractManager():
    def __init__(self, contract_list=[]):
        self.__contracts = {}
        for contract in contract_list:
            self.add_contract(contract)

    def add_contract(self, contract):
        self.__contracts[contract.name] = contract

    def remove_contract(self, contract):
        self.__contracts.pop(contract.name, None)

    def get_contract(self, contract_name):
        contract = self.__contracts.get(contract_name)
        if contract is None:
            raise ContractNotFound("Contract not found ({})".format(contract_name))
        else:
            return contract

    def get_contracts(self):
        return self.__contracts.values()

    def get_contract_names(self):
        return self.__contracts.keys()


# class ContractManager():
#     def __init__(self, contract_list):
#         self._contracts = contract_list
#         self._ethereum_connection = self._contracts[0]._contract_connection._eth_conn
#         self.__init_struct_commit_processors()
#         self.__init_struct_schedule_processors()
#         self.__init_struct_handlers()

#     def __init_struct_handlers(self):
#         self._handlers = {}
#         for contract in self._contracts:
#             self._handlers[contract._address] = contract._handlers

#     def add_new_contract(self, contract):
#         self._contracts.append(contract)
#         self._commit_processors.update(contract._commit_processors)
#         self._schedule_processors.update(contract._schedule_processors)
#         self._handlers[contract._address] = contract._handlers

#     def __init_struct_commit_processors(self):
#         self._commit_processors = {}
#         for contract in self._contracts:
#             self._commit_processors.update(contract._commit_processors)

#     def __init_struct_schedule_processors(self):
#         self._schedule_processors = {}
#         for contract in self._contracts:
#             self._schedule_processors.update(contract._schedule_processors)

#     def handle_event(self, event):
#         for contract in self._contracts:
#             if contract.is_my_event(event):
#                 return contract.handle_event(event)
#         return None

#     # def handle_event(self, event):
#     #     handler = self._get_handlers_by_event(event)
#     #     return handler(event)

#     def is_handleable(self, event):
#         return event.get("address") in self._handlers

#     def _get_handlers_by_event(self, event):
#         handlers = self._handlers[event.get("address")]
#         handler = handlers.get(event.get("topic0"))
#         return handler

#     def _get_commit_processor_by_opcode(self, opcode):
#         return self._commit_processors.get(opcode)

#     def _get_schedule_processor_by_opcode(self, opcode):
#         return self._schedule_processors.get(opcode)

#     def handle_commit(self, commit, optional_data={}):
#         commit_processor = self._get_commit_processor_by_opcode(commit.opcode)
#         logger.info("commit class {}".format(commit_processor.__class__.__name__))
#         commit_processor.process(commit, **optional_data)

#     def handle_schedule(self, schedule, optional_data={}):
#         schedule_processor = self._get_schedule_processor_by_opcode(schedule.opcode)
#         return schedule_processor.process(schedule, **optional_data)

#     def go_back(self, commit):
#         commit_processor = self._get_commit_processor_by_opcode(commit.opcode)
#         commit_processor.apply_old(commit)
