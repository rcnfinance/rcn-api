from .commit_processor import CommitProcessor
from ..models import Loan
from models import Schedule

class LentCommitProcessor(CommitProcessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opcode = "lent"

    def process(self, commit, *args, **kwargs):
        data = commit.data
        opcode = commit.opcode
        
        loan = Loan.objects(index=data['loan']).first()
        assert loan.status == 0, "Try to apply lend on already lent loan"
        loan.status = 1
        loan.lender = data['lender']
        loan.due_time = data["due_time"]
        loan.interest_timestamp = data["interest_timestamp"]
        loan.commits.append(commit)
        loan.save()
        self.logger.info("Processing {} {} loan {}".format(commit.order, commit.opcode, loan.index))

        # add schedule for in_debt
        schedule = Schedule()
        schedule.timestamp = loan.due_time
        schedule.opcode = "check_in_debt"
        schedule.data = {
            "loan": loan.index
        }
        schedule.save()
        self.logger.info(
            "Created schedule {} at {} for loan {}".format(schedule.opcode, schedule.timestamp, loan.index))

        commit.loan = loan.to_dict()
        commit.save()