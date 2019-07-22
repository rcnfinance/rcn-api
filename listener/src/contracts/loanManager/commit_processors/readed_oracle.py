from contracts.commit_processor import CommitProcessor
from models import OracleHistory


class ReadedOracle(CommitProcessor):
    def __init__(self):
        self.opcode = "readed_oracle_loan_manager"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        oh = OracleHistory()
        oh.id = data.get("id")
        oh.tokens = data.get("tokens")
        oh.equivalent = data.get("equivalent")
        oh.timestamp = data.get("timestamp")

        oh.save()
