from models import ERC20D, Claim
from contracts.commit_processor import CommitProcessor


class ClaimedTransfer(CommitProcessor):
    def __init__(self):
        self.opcode = "claimed_transfer_ERC20D"

    def process(self, commit, *args, **kwargs):
        data = commit.data   
           
        try:
            erc20d = ERC20D.objects.get(id=data["contractAddress"])

            claimFrom = erc20d.claimers.objects.get(id=data["from"])
            claimTo = erc20d.claimers.objects.get(id=data["to"])

            new_claimedFrom = int(claimFrom.claimedAmount) - int(data.get("value"))
            new_claimedTo = int(claimTo.claimedAmount) + int(data.get("value"))

            claimFrom.claimedAmount = str(new_claimedFrom)
            claimFrom.claimedAmount = str(new_claimedTo)
            
            
            commit.save()
            claimFrom.save()
            claimTo.save()
        except ERC20D.DoesNotExist:
            self.logger.warning("ERC20D with address {} does not exist".format(data["contractAddress"]))