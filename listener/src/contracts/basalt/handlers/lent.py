import web3

from .event_handler import EventHandler
import utils
from ..models import Commit
from ..models import Loan
from utils import get_internal_interest

import logging
log = logging.getLogger(__name__)


class Lent(EventHandler):
    signature = 'Lent(uint256,address,address)'
    signature_hash = web3.Web3.sha3(text=signature)

    def _parse(self):
        data = self._event.get('data')[2:]
        splited_args = utils.split_every(64, data)
        self._index = utils.to_int(splited_args[0])
        self._lender = utils.to_address(splited_args[1])
        self._cosigner = utils.to_address(splited_args[2])
        self._block_number = self._event.get('blockNumber')
        self._transaction = self._event.get('transactionHash').hex()

    def do(self):
        self._logger.info("Apply handler")
        loan = Loan.objects(index=self._index).first()
        block_timestamp = self._block_timestamp()

        commits = []
        # Commit lend
        commit_lent = Commit()
        data_lent = {}
        data_lent['lender'] = self._lender
        data_lent['loan'] = self._index
        data_lent["due_time"] = str(block_timestamp + int(loan.dues_in))
        data_lent["interest_timestamp"] = str(block_timestamp)

        commit_lent.opcode = "lent"
        commit_lent.timestamp = block_timestamp
        commit_lent.proof = self._transaction
        commit_lent.data = data_lent

        commits.append(commit_lent)

        # Commit interest
        if int(loan.cancelable_at) > 0:
            commit_interest = Commit()
            data_interest = {}
            data_interest["loan"] = self._index
            data_interest["interest_timestamp"] = str(block_timestamp)
            timestamp = block_timestamp + int(loan.cancelable_at)
            interest_data = get_internal_interest(
                timestamp,
                data_lent["interest_timestamp"],
                loan.interest,
                loan.punitory_interest,
                data_lent["due_time"],
                loan.paid,
                loan.amount,
                loan.interest_rate,
                loan.interest_rate_punitory
            )
            if isinstance(interest_data, dict):
                data_interest.update(interest_data)

            commit_interest.opcode = "interest"
            commit_interest.timestamp = block_timestamp
            commit_interest.proof = self._transaction
            commit_interest.data = data_interest
            commits.append(commit_interest)

        return commits
    