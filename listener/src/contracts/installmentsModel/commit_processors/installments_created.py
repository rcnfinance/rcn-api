from models import Config
from contracts.commit_processor import CommitProcessor


class InstallmentsCreated(CommitProcessor):
    def __init__(self):
        self.opcode = "created_installments"

    def process(self, commit, *args, **kwargs):
        data = commit.new_data

        config = Config()

        old_data = {
            "id": data.get("id")
        }

        config.id = data["id"]
        del data["id"]
        data["cuota"] = str(data["cuota"])
        config.data = data

        commit.old_data = old_data
        commit.save()
        config.save()

    def apply_old(self, commit, *args, **kwargs):
        data = commit.old_data

        config = Config.objects.get(id=data.get("id"))

        config.delete()
        commit.delete()
