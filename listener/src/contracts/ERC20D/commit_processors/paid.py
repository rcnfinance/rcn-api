from models import ERC20D
from contracts.commit_processor import CommitProcessor


class Paid(CommitProcessor):
    def __init__(self):
        self.opcode = "paid_ERC20D"

    def process(self, commit, *args, **kwargs):
        data = commit.data
 
        try:
            erc20d = ERC20D.objects.get(id=data["contractAddress"])
            new_paid = int(erc20d.paid) + int(data.get("value"))
            erc20d.paid = str(new_paid)
            
            commit.save()
            erc20d.save()
        except ERC20D.DoesNotExist:
            self.logger.warning("ERC20D with address {} does not exist".format(data["contractAddress"]))