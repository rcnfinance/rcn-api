from models import OracleRate
from contracts.commit_processor import CommitProcessor


class Provide(CommitProcessor):
    def __init__(self):
        self.opcode = "provide_oracleFactory"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        oracleRate = OracleRate()

        oracleRate.oracle = data.get("oracle")
        oracleRate.signer = data.get("signer")
        oracleRate.rate = data.get("rate")

        print(commit)
       
        commit.save()
        oracleRate.save()