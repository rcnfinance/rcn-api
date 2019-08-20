from models import OracleHistory
from contracts.commit_processor import CommitProcessor


class ReadedOracle(CommitProcessor):
    def __init__(self):
        self.opcode = "readed_oracle_debt_engine"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        oracle = OracleHistory()
        oracle.id = data.get("id")
        oracle.timestamp = data.get("timestamp")
        oracle.tokens = data.get("tokens")
        oracle.equivalent = data.get("equivalent")

        commit.save()
        oracle.save()

    def apply_old(self, commit, *args, **kwargs):
        pass
