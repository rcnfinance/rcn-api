import logging

from models import Commit, Loan
from clock import Clock

logger = logging.getLogger(__name__)

class Processor:
    nonce = 0
    clock = Clock()

    def pull_nonce(self):
        t = self.nonce
        self.nonce += 1
        return t
    
    def execute(self, commit):
        self.clock.time = commit.timestamp

        data = commit.data
        opcode = commit.opcode
        commit.order = self.pull_nonce()

        logger.info("Processing {}".format(commit.order))

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
            return

        if opcode == "lent":
            logger.info(data)
            loan = Loan.objects(index=data['loan']).first()
            assert loan.status == 0, "Try to apply lend on already lent loan"
            loan.status = 1
            loan.lender = data['lender']
            loan.commits.append(commit)
            loan.save()
            return

        if opcode == "transfer":
            loan = Loan.objects(index=data['loan']).first()
            commit['from'] = loan.lender
            loan.lender = data['to']
            loan.commits.append(commit)
            loan.save()
            return

        assert False