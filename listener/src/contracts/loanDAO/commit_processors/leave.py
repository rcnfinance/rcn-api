from models import Pool, Participant
from contracts.commit_processor import CommitProcessor


class Leave(CommitProcessor):
    def __init__(self):
        self.opcode = "leave_loanDAO"

    def process(self, commit, *args, **kwargs):
        data = commit.data

        try:
            pool = Pool.objects.get(id=data["poolId"])
            new_raised = int(pool.raised) - int(data.get("tokens"))
            pool.raised = str(new_raised)
   
            participant = pool.participants.get(lender=data["lender"])
            new_joined = int(participant.balance) - int(data.get("tokens"))
            participant.balance = str(new_joined)

            
            commit.save()
            pool.save()
        except Pool.DoesNotExist:
            self.logger.warning("Pool with id {} does not exist".format(data["poolId"])) 
        except Participant.DoesNotExist:
             self.logger.warning("Participant with id {} , nothing to leave".format(data["lender"]))
    