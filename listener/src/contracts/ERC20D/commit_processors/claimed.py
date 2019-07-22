from models import ERC20D, Claim
from contracts.commit_processor import CommitProcessor


class Claimed(CommitProcessor):
    def __init__(self):
        self.opcode = "claimed_ERC20D"

    def process(self, commit, *args, **kwargs):
        data = commit.data
 
        try:
            erc20d = ERC20D.objects.get(id=data["contractAddress"])

            claim = erc20d.claimers.get(id=data["from"])

            new_claimed = int(claim.claimedAmount) + int(data.get("value"))
            claim.claimedAmount = str(new_claimed)

            commit.save()
            claim.save()
        except ERC20D.DoesNotExist:
            self.logger.warning("ERC20D with address {} does not exist".format(data["contractAddress"]))
        except Claim.DoesNotExist:
            claimer = Claim()
            claimer.lender = data["from"]
            claimer.claimed_amount = data["value"]
            erc20d.claimers.append(claimer)
            
            commit.save()
            erc20d.save()   