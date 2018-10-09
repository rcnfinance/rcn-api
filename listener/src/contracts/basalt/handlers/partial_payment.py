import web3
from .event_handler import EventHandler
import utils
from ..models import Commit
from ..models import Loan
from utils import get_internal_interest

class PartialPayment(EventHandler):
    signature = 'PartialPayment(uint256,address,address,uint256)'
    signature_hash = web3.Web3.sha3(text=signature)

    def _parse(self):
        data = self._event.get('data')[2:]
        splited_args = utils.split_every(64, data)
        self._index = utils.to_int(splited_args[0])
        self._sender = utils.to_address(splited_args[1])
        self._from = utils.to_address(splited_args[2])
        self._amount = str(utils.to_int(splited_args[3]))
        self._block_number = self._event.get('blockNumber')
        self._transaction = self._event.get('transactionHash').hex()

    def do(self):
        self._logger.info("Apply handler")
        loan = Loan.objects(index=self._index).first()
        block_timestamp = self._block_timestamp()
        commits = []
        # Commit pay
        commit_pay = Commit()

        data_pay = {}
        data_pay['loan'] = self._index
        data_pay['sender'] = self._sender
        data_pay['from'] = self._from
        data_pay['amount'] = self._amount

        commit_pay.opcode = "partial_payment"
        commit_pay.timestamp = block_timestamp
        commit_pay.proof = self._transaction
        commit_pay.data = data_pay
        # commit_pay.loan = loan.to_dict()

        interest_data = get_internal_interest(
            block_timestamp,
            loan.interest_timestamp,
            loan.interest,
            loan.punitory_interest,
            loan.due_time,
            loan.paid,
            loan.amount,
            loan.interest_rate,
            loan.interest_rate_punitory
        )

        if isinstance(interest_data, dict):
            interest_data2 = get_internal_interest(
                block_timestamp,
                interest_data.get("interest_timestamp"),
                interest_data.get("interest"),
                interest_data.get("punitory_interest"),
                loan.due_time,
                loan.paid,
                loan.amount,
                loan.interest_rate,
                loan.interest_rate_punitory
            )
            if isinstance(interest_data2, dict):
                interest_data = interest_data2

        if isinstance(interest_data, dict):
            commit_interest = Commit()
            commit_interest.opcode = "interest"
            commit_interest.timestamp = block_timestamp
            commit_interest.proof = self._transaction
            commit_interest.loan = loan.to_dict()

            data_interest = {}
            data_interest["loan"] = self._index
            data_interest.update(interest_data)

            commit_interest.data = data_interest

            commits.append(commit_interest)

        commits.append(commit_pay)

        return commits
