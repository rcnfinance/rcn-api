from .commit_processor import CommitProcessor
from ..models import Loan
from models import Schedule

class LoanRequestCommitProcessor(CommitProcessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opcode = "loan_request"
    
    def process(self, commit, *args, **kwargs):
        clock = kwargs.get("clock")
        data = commit.data
        opcode = commit.opcode

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
        self.logger.info("Processing {} {} created loan {}".format(commit.order, commit.opcode, loan.index))

        # Schedule check expiration
        # only schedule events for the next 1000 years
        if int(loan.expiration_requests) - clock.time < 31536000000:
            schedule = Schedule()
            schedule.timestamp = loan.expiration_requests
            schedule.opcode = 'check_expired'
            schedule.data = {}
            schedule.data['loan'] = loan.index
            schedule.save()
            self.logger.info("Created schedule {} at {} for loan {}".format(schedule.opcode, schedule.timestamp, loan.index))

        commit.loan = loan.to_dict()
        commit.save()
