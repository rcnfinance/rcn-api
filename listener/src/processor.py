import os
import logging
from db import connection
from models import Schedule
from clock import Clock
import utils

logger = logging.getLogger(__name__)


class NonceSequencer:
    def __init__(self, initial=0):
        self._nonce = 0

    def pull(self):
        nonce = self._nonce
        self._nonce += 1

        return nonce

    @property
    def nonce(self):
        return self._nonce
    

class Processor:
    def __init__(self, buffer, contract_manager):
        self.buffer = buffer
        self._contract_manager = contract_manager
        self.nonce_sequencer = NonceSequencer()

        self.clock = Clock()
        self.clock.reset()

        self.buffer.subscribe_changes(self.new_entries)

    def new_entries(self, events, timestamp):
        # pull block y lo toma como argumento el handle_event
        block = None
        tx = None
        for event in events:
            if block is None or event.get("blockNumber") > block.get("number"):
                # print("pull block", event.get("blockNumber"))
                # block = self._contract_manager._ethereum_connection.w3.eth.getBlock(event.get("blockNumber"))
                block = utils.getBlock(self._contract_manager._ethereum_connection.w3, event.get("blockNumber"))
            if tx is None or event.get("transactionHash").hex() != tx.get("hash").hex():
                # print("pull tx", event.get("transactionHash").hex())
                tx = self._contract_manager._ethereum_connection.w3.eth.getTransaction(event.get("transactionHash").hex())
            handler = self._contract_manager.handle_event(event, block, tx)
            if handler:
                commits = handler.handle()
                self.execute(commits)

        self._advance_time(timestamp)

    def log(self, msg):
        logger.info('PTime: {} - PNonce: {} - {}'.format(self.clock.time, self.nonce_sequencer.nonce, msg))

    def _advance_time(self, target):
        # For every second between the origin and the target
        # we must check the scheduled operations
        self.log('Requested advance time to {} delta {}'.format(target, target - self.clock.time))
        while self.clock < target:
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

    def _evaluate_schedule(self, schedule):
        additional_data = {
            "clock": self.clock
        }

        return self._contract_manager.handle_schedule(schedule)

    def execute(self, commits):
        for commit in commits:
            self._advance_time(commit.timestamp)
            commit.order = self.nonce_sequencer.pull()

            additional_data = {
                "clock": self.clock
            }

            self._contract_manager.handle_commit(commit, additional_data)

            # if commit.timestamp < self.clock.time:
            #     message = 'Old commit loaded {} {} {} {}'.format(
            #         commit.timestamp, self.clock.time, commit.timestamp - self.clock.time, commit.opcode
            #     )
            #     logger.info(message)
            #     self.buffer.integrity_broken()
            #     return
            # else:
            #     self._advance_time(commit.timestamp)
            #     commit.order = self.nonce_sequencer.pull()

            #     additional_data = {
            #         "clock": self.clock
            #     }

            #     self._contract_manager.handle_commit(commit, additional_data)
