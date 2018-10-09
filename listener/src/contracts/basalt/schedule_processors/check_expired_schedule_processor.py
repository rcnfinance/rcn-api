from .schedule_processor import ScheduleProcessor
from ..models import Loan
from models import Commit

class CheckExpiredScheduleProcessor(ScheduleProcessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opcode = "check_expired"

    def process(self, schedule, *args, **kwargs):
        data = schedule.data
        opcode = schedule.opcode
        loan = Loan.objects(index=data["loan"]).first()
        self.logger.info('Evaluate schedule {} loan {} at {}'.format(opcode, loan.index, schedule.timestamp))
        if loan.status == 0:
            commit = Commit()
            commit.opcode = "loan_expired"
            commit.timestamp = schedule.timestamp
            commit.data = {}
            commit.data['loan'] = loan.index
            return [commit]
        else:
            return []