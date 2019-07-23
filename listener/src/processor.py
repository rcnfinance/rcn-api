import os
import logging
import datetime
from models import Commit, Loan, Schedule
from clock import Clock
from mongoengine import connect
from handlers import get_class_by_event

logger = logging.getLogger(__name__)


class Processor:
    last_seen = 0

    def __init__(self, buffer):
        self.buffer = buffer
        self.nonce = 0
        self.clock = Clock()
        self.clock.reset()
        self.buffer.subscribe_changes(self.new_entries)
        self.buffer.subscribe_integrity(self.integrity_error)

    def new_entries(self, timestamp):
        for event in self.buffer.registry:
            if event.position > self.last_seen:
                eventClass = get_class_by_event(event.data)
                logger.info('Apply event {} position {} index {}'.format(type(eventClass).__name__, event.position, self.buffer.registry.index(event)))
                self.last_seen = event.position
                commits = eventClass.do()
                if commits:
                    self.execute(commits)

        self._advance_time(timestamp)

    def integrity_error(self):
        mongo_db = os.environ.get("MONGO_DB", "rcn")
        mongo_host = os.environ.get("MONGO_HOST", "mongo")

        self.connection = connect(db=mongo_db, host=mongo_host)
        self.connection.drop_database(mongo_db)
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
                self.clock.advance_to(int(op.timestamp))
                commits = self._evaluate_schedule(op)
                if commits:
                    self.execute(commits)
                # Delete the runned schedule
                op.delete()
            else:
                self.clock.advance_to(target)

    def _evaluate_schedule(self, schedule):
        data = schedule.data
        opcode = schedule.opcode

        if opcode == "check_expired":
            loan = Loan.objects(index=data["loan"]).first()
            self.log('Evaluate schedule {} loan {} at {}'.format(opcode, loan.index, schedule.timestamp))
            if loan.status == 0:
                commit = Commit()
                commit.opcode = "loan_expired"
                commit.timestamp = schedule.timestamp
                commit.data = {}
                commit.data['loan'] = loan.index
                commit.id_loan = loan.index
                return [commit]
            else:
                return []

        if opcode == "check_in_debt":
            loan = Loan.objects(index=data["loan"]).first()
            self.log('Evaluate schedule {} loan {} at {}'.format(opcode, loan.index, schedule.timestamp))
            timestamp_now = datetime.datetime.utcnow().timestamp()
            loan_dues_time = int(loan.due_time)
            self.log("timestamp_now: {}, loan_dues_in: {}".format(timestamp_now, loan_dues_time))
            if loan.status == 1 and timestamp_now > loan_dues_time:  # LENT
                self.log("loan {} in debt".format(loan.index))
                commit = Commit()
                commit.opcode = "loan_in_debt"
                commit.timestamp = schedule.timestamp
                commit.data = {
                    "loan": loan.index
                }
                commit.id_loan = self._index
                return [commit]
            else:
                return []

        return []

    def execute(self, commits):
        for commit in commits:
            if int(commit.timestamp) < self.clock.time:
                logger.info('Old commit loaded {} {} {} {}'.format(commit.timestamp, self.clock.time, commit.timestamp - self.clock.time, commit.opcode))
                self.buffer.integrity_broken()
                return
            else:
                self._advance_time(int(commit.timestamp))

                data = commit.data
                opcode = commit.opcode
                commit.order = self._pull_nonce()

                if opcode == "loan_request":
                    loan = Loan()
                    loan.index = data['index']
                    loan.created = data['created']
                    loan.creator = data['creator']
                    loan.borrower = data['borrower']
                    loan.oracle = data['oracle']
                    loan.amount = data['amount']
                    loan.interest_rate = data['interest_rate']
                    loan.interest_rate_punitory = data['interest_rate_punitory']
                    loan.dues_in = data['dues_in']
                    loan.currency = data['currency']
                    loan.cancelable_at = data['cancelable_at']
                    loan.expiration_requests = data['expiration_requests']
                    commit.save()
                    loan.save()
                    self.log("Processing {} {} created loan {}".format(commit.order, commit.opcode, loan.index))

                    # Schedule check expiration
                    # only schedule events for the next 1000 years
                    if int(loan.expiration_requests) - self.clock.time < 31536000000:
                        schedule = Schedule()
                        schedule.timestamp = loan.expiration_requests
                        schedule.opcode = 'check_expired'
                        schedule.data = {}
                        schedule.data['loan'] = loan.index
                        schedule.save()
                        self.log("Created schedule {} at {} for loan {}".format(schedule.opcode, schedule.timestamp, loan.index))

                if opcode == "loan_expired":
                    loan = Loan.objects(index=data['loan']).first()
                    assert loan.status == 0, "The loan was lent"
                    assert int(loan.expiration_requests) <= self.clock, "The loan is not expired" # < or <= ? check contract
                    commit.save()
                    loan.save()
                    self.log("Processing {} {} loan {}".format(commit.order, commit.opcode, loan.index))

                if opcode == "lent":
                    loan = Loan.objects(index=data['loan']).first()
                    assert loan.status == 0, "Try to apply lend on already lent loan"
                    loan.status = 1
                    loan.lender = data['lender']
                    loan.due_time = data["due_time"]
                    commit.save()
                    loan.save()
                    self.log("Processing {} {} loan {}".format(commit.order, commit.opcode, loan.index))

                    # add schedule for in_debt
                    schedule = Schedule()
                    schedule.timestamp = loan.due_time
                    schedule.opcode = "check_in_debt"
                    schedule.data = {
                        "loan": loan.index
                    }
                    schedule.save()
                    self.log(
                        "Created schedule {} at {} for loan {}".format(schedule.opcode, schedule.timestamp, loan.index))

                if opcode == "loan_in_debt":
                    loan = Loan.objects(index=data['loan']).first()
                    assert loan.status == 1, "The loan was paid or destroyed"
                    commit.save()
                    loan.save()
                    self.log("Processing {} {} loan {}".format(commit.order, commit.opcode, loan.index))

                if opcode == "transfer":
                    loan = Loan.objects(index=data['loan']).first()
                    data['from'] = loan.lender
                    loan.lender = data['to']
                    commit.save()
                    loan.save()
                    self.log("Processing {} {} loan {} from {} to {}".format(commit.order, commit.opcode, loan.index, data['from'], data['to']))

                if opcode == "approved_loan":
                    loan = Loan.objects(index=data["loan"]).first()
                    loan.approbations.append(data["approved_by"])
                    commit.save()
                    loan.save()
                    self.log("Processing {} {} loan {} by {}".format(commit.order, commit.opcode, loan.index, data['approved_by']))

                if opcode == "destroyed_loan":
                    loan = Loan.objects(index=data["loan"]).first()
                    loan.status = 2
                    commit.save()
                    loan.save()
                    self.log("Processing {} {} loan {}".format(commit.order, commit.opcode, loan.index))

                if opcode == "partial_payment":
                    loan = Loan.objects(index=data["loan"]).first()
                    loan.paid = str(int(loan.paid) + int(commit.data.get("amount")))
                    commit.save()
                    loan.save()
                    self.log("Processing {} {} loan {}".format(commit.order, commit.opcode, loan.index))

                if opcode == "total_payment":
                    loan = Loan.objects(index=data["loan"]).first()
                    loan.status = 3
                    commit.save()
                    loan.save()
                    self.log("Processing {} {} loan {}".format(commit.order, commit.opcode, loan.index))
