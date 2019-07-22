import logging


logger = logging.getLogger(__name__)


class ContractManager():
    def __init__(self, contract_list):
        self._contracts = contract_list
        self._ethereum_connection = self._contracts[0]._contract_connection._eth_conn
        self.__init_struct_commit_processors()
        self.__init_struct_schedule_processors()

    def __init_struct_commit_processors(self):
        self._commit_processors = {}
        for contract in self._contracts:
            self._commit_processors.update(contract._commit_processors)

    def __init_struct_schedule_processors(self):
        self._schedule_processors = {}
        for contract in self._contracts:
            self._schedule_processors.update(contract._schedule_processors)

    def handle_event(self, event):
        for contract in self._contracts:
            if contract.is_my_event(event):
                return contract.handle_event(event)
        return None

    def _get_commit_processor_by_opcode(self, opcode):
        return self._commit_processors.get(opcode)

    def _get_schedule_processor_by_opcode(self, opcode):
        return self._schedule_processors.get(opcode)

    def handle_commit(self, commit, optional_data={}):
        commit_processor = self._get_commit_processor_by_opcode(commit.opcode)
        logger.info("commit class {}".format(commit_processor.__class__.__name__))
        commit_processor.process(commit, **optional_data)

    def handle_schedule(self, schedule, optional_data={}):
        schedule_processor = self._get_schedule_processor_by_opcode(schedule.opcode)
        return schedule_processor.process(schedule, **optional_data)