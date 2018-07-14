import logging

from models import Commit, Loan
from clock import Clock

logger = logging.getLogger(__name__)

class Processor:
    clock = Clock()
    
    def advance_time(self, target):
        

    def execute(self, commit):
        self.clock.time = commit.timestamp

        data = commit.data
        opcode = commit.opcode

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
            loan.save()
            return

        if opcode == "lent":
            logger.info(data)
            loan = Loan.objects(index=data['loan']).first()
            assert loan.status == 0, "Try to apply lend on already lent loan"
            loan.status = 1
            loan.lender = data['lender']
            loan.save()
            return

        if opcode == "transfer":
            loan = Loan.objects(index=data['loan']).first()
            loan.lender = data['to']
            loan.save()
            return

        assert False