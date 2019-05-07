import os
import logging
from db import connection
from models import Schedule
from clock import Clock

logger = logging.getLogger(__name__)


class Processor:
    last_seen = 0

    def __init__(self, buffer, contract_manager):
        self.buffer = buffer
        self._contract_manager = contract_manager
        self.nonce = 0
        self.clock = Clock()
        self.clock.reset()
        self.buffer.subscribe_changes(self.new_entries)
        self.buffer.subscribe_integrity(self.integrity_error)

    def new_entries(self, timestamp):
        for event in self.buffer.registry:
            if event.position > self.last_seen:
                handler = self._contract_manager.handle_event(event.data)
                self.last_seen = event.position
                if handler:
                    commits = handler.handle()
                    self.execute(commits)

        self._advance_time(timestamp)

    def integrity_error(self):
        connection.drop_database(os.environ.get("MONGO_DB"))
        self.clock.reset()
        self.nonce = 0
        self.last_seen = 0

    def _pull_nonce(self):
        t = self.nonce
        self.nonce += 1
        return t

    def log(self, msg):
        logger.info('PTime: {} - PNonce: {} - {}'.format(self.clock.time, self.nonce, msg))

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
            if commit.timestamp < self.clock.time:
                message = 'Old commit loaded {} {} {} {}'.format(
                    commit.timestamp, self.clock.time, commit.timestamp - self.clock.time, commit.opcode
                )
                logger.info(message)
                self.buffer.integrity_broken()
                return
            else:
                self._advance_time(commit.timestamp)
                commit.order = self._pull_nonce()

                additional_data = {
                    "clock": self.clock
                }

                self._contract_manager.handle_commit(commit, additional_data)
