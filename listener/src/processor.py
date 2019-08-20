import logging
import operator
from web3.eth import HexBytes
from web3.datastructures import AttributeDict
from models import Schedule
from models import Commit
from clock import Clock

logger = logging.getLogger(__name__)


class Processor:
    def __init__(self, contract_manager):
        self._contract_manager = contract_manager
        self.nonce = 0
        self.clock = Clock()

    def __log_to_attdict(self, log):
        topics = []
        for i in range(4):
            item_name = "topic{}".format(i)
            topic = operator.getitem(log, item_name)
            if topic:
                topics.append(HexBytes(topic))

        log["topics"] = topics
        log["logIndex"] = 0
        log['transactionIndex'] = 0
        log['transactionHash'] = HexBytes(log.get("transactionHash"))
        return AttributeDict(log)

    def __get_contract_by_log(self, log):
        #utilizar cache
        contract = list(
            filter(
                lambda contract: log.get("address") in contract.address,
                self._contract_manager.get_contracts()
            )
        )
        # Asumo que tiene que devolver una lista con un solo contract
        if contract:
            return contract[0]
        else:
            return None

    def process(self, blocks):
        if blocks:
            logger.info("process {} blocks: from: {} to {}".format(len(blocks), blocks[0].get("number"), blocks[-1].get("number")))
        for block in blocks:
            for log in block.get("logs") or []:
                # logger.info(log)
                contract = self.__get_contract_by_log(log)
                if contract:
                    att_log = self.__log_to_attdict(log)
                    commits = contract.handle_event(att_log)
                    print(contract.__class__.__name__)
                    for commit in commits:
                        self._advance_time(commit.timestamp)
                        commit.order = self._pull_nonce()
                        contract.handle_commit(commit)
                    # self._execute_commits(commits)
            self._advance_time(int(block.get("timestamp")))

    def on_new_blocks(self, blocks):
        self.process(blocks)

    def __get_contract_by_commit(self, commit):
        for contract in self._contract_manager.get_contracts():
            if commit.opcode in contract.get_opcodes_commit_processors():
                return contract

    def on_fork(self, blocks):
        # restore to blocks
        commits = Commit.objects.filter(block_number__gte=blocks[0].get("number"))
        if commits:
            for commit in commits:
                contract = self.__get_contract_by_commit(commit)
                contract.rollback_commit(commit)
                self._decrease_nonce()
                # commit.delete()
            self.clock.set_back(int(blocks[0].get("timestamp")))

    def _pull_nonce(self):
        t = self.nonce
        self.nonce += 1
        return t

    def _decrease_nonce(self):
        self.nonce -= 1
        return self.nonce

    def log(self, msg):
        logger.info('PTime: {} - PNonce: {} - {}'.format(self.clock.time, self.nonce, msg))

    def _advance_time(self, target):
        # For every second between the origin and the target
        # we must check the scheduled operations
        self.log('Requested advance time to {} delta {}'.format(target, target - self.clock.time))
        while self.clock.time < target:
            op = Schedule.objects(timestamp__lte=target).order_by('timestamp').first()
            if op:
                self.log('Handling schedule {} scheduled {}'.format(op.opcode, op.timestamp))
                self.clock.advance_to(op.timestamp)
                commits = self._evaluate_schedule(op)
                if commits:
                    self.execute(commits)
                # Delete the runned schedule
                op.delete()
            else:
                self.clock.advance_to(target)

    def _deacrease_time(self, target):
        while self.clock > target:
            op = Schedule.objects(timestamp__gte=target).order_by("+timestamp").first()
            if op:
                self.clock.set_back(op.timestamp)
                op.delete()
            else:
                self.clock.set_back(target)

    def _evaluate_schedule(self, schedule):
        additional_data = {
            "clock": self.clock
        }

        return self._contract_manager.handle_schedule(schedule, additional_data)

    def _execute_commits(self, commits):
        for commit in commits:
            self._advance_time(commit.timestamp)
            commit.order = self._pull_nonce()

            additional_data = {
                "clock": self.clock
            }

            self._contract_manager.handle_commit(commit, additional_data)
