#from models import Loan
from contracts.commit_processor import CommitProcessor


class ConvertPay(CommitProcessor):
    def __init__(self):
        self.opcode = "convert_pay_collateral"

    def process(self, commit, *args, **kwargs):
        pass