import logging

from models import Commit, Loan, Schedule

logger = logging.getLogger(__name__)

class Processor:
    def __init__(self, nonce=0, clock=0):
        self.nonce = nonce
        self.clock = clock

    def _pull_nonce(self):
        t = self.nonce
        self.nonce += 1
        return t

    def _advance_time(self, target):
        # For every second between the origin and the target
        # we must check the scheduled operations
        while self.clock < target:
            op = Schedule.objects(timestamp__lte=target).order_by('-timestamp').first()
            if op:
                logger.info('Handling schedule {}'.format(op.opcode))
                self.clock = op.timestamp
                commits = self._evaluate_schedule(op)
                # for commit in commits:
                #     self.execute(commit)
                self.execute(commits)
                # Delete the runned schedule
                op.delete()
            else:
                self.clock = target

    def _evaluate_schedule(self, schedule):
        data = schedule.data
        opcode = schedule.opcode

        if opcode == "check_expired":
            loan = Loan.objects(index=data["loan"]).first()
            if loan.status == 0:
                commit = Commit()
                commit.opcode = "loan_expired"
                commit.timestamp = schedule.timestamp
                commit.data = {}
                commit.data['loan'] = loan.index
                return [commit]
            else:
                return []

        return []

    def execute(self, commits):
        for commit in commits:
            self._advance_time(commit.timestamp)

            data = commit.data
            opcode = commit.opcode
            commit.order = self._pull_nonce()

            logger.info("Processing {} {}".format(commit.order, commit.opcode))

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
                loan.commits.append(commit)
                loan.save()

                # Schedule check expiration
                # only schedule events for the next 1000 years
                if int(loan.expiration_requests) - self.clock < 31536000000:
                    schedule = Schedule()
                    schedule.timestamp = loan.expiration_requests
                    schedule.opcode = 'check_expired'
                    schedule.data = {}
                    schedule.data['loan'] = loan.index
                    schedule.save()

                return

            if opcode == "loan_expired":
                loan = Loan.objects(index=data['loan']).first()
                assert loan.status == 0, "The loan was lent"
                assert int(loan.expiration_requests) <= self.clock, "The loan is not expired" # < or <= ? check contract
                loan.commits.append(commit)
                loan.save()
                return

            if opcode == "lent":
                loan = Loan.objects(index=data['loan']).first()
                assert loan.status == 0, "Try to apply lend on already lent loan"
                loan.status = 1
                loan.lender = data['lender']
                loan.commits.append(commit)
                loan.save()
                return

            if opcode == "transfer":
                loan = Loan.objects(index=data['loan']).first()
                data['from'] = loan.lender
                loan.lender = data['to']
                loan.commits.append(commit)
                loan.save()
                return

            if opcode == "approved_loan":
                loan = Loan.objects(index=data["loan"]).first()
                loan.approbations.append(data["approved_by"])
                loan.commits.append(commit)
                loan.save()
                return

            if opcode == "destroyed_loan":
                loan = Loan.objects(index=data["loan"]).first()
                loan.status = 2
                loan.commits.append(commit)
                loan.save()
                return

            if opcode == "partial_payment":
                # DO MORE
                loan = Loan.objects(index=data["loan"]).first()

                loan.commits.append(commit)
                loan.save()
                return

            if opcode == "total_payment":
                loan = Loan.objects(index=data["loan"]).first()
                loan.status = 3
                loan.commits.append(commit)
                loan.save()
                return

            assert False