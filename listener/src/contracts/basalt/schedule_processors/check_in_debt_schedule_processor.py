import datetime
from .schedule_processor import ScheduleProcessor
from ..models import Loan
from models import Commit

class CheckInDebtScheduleProcessor(ScheduleProcessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opcode = "check_in_debt"

    def process(self, schedule, *args, **kwargs):
        data = schedule.data
        opcode = schedule.opcode

        loan = Loan.objects(index=data["loan"]).first()
        self.logger.info('Evaluate schedule {} loan {} at {}'.format(opcode, loan.index, schedule.timestamp))
        timestamp_now = datetime.datetime.utcnow().timestamp()
        loan_dues_time = int(loan.due_time)
        self.logger.info("timestamp_now: {}, loan_dues_in: {}".format(timestamp_now, loan_dues_time))
        if loan.status == 1 and timestamp_now > loan_dues_time:  # LENT
            self.logger.info("loan {} in debt".format(loan.index))
            commit = Commit()
            commit.opcode = "loan_in_debt"
            commit.timestamp = schedule.timestamp
            commit.data = {
                "loan": loan.index
            }
            return [commit]
        else:
            return []