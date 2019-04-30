import json
from models import Debt, Config
from contracts.commit_processor import CommitProcessor


class InstallmentsCreated(CommitProcessor):
    def __init__(self):
        self.opcode = "created_installments"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        config = Config()

        config.id = data["id"]
        del data["id"]
        data["cuota"] = str(data["cuota"])
        config.data = data

        config.commits.append(commit)

        config.save()
