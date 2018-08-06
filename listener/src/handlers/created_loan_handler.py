import web3
import logging

from datetime import datetime as dt
from multiprocessing import Manager
from multiprocessing import Process
from multiprocessing import ProcessError
from .event_handler import EventHandler
from models import Commit
from handlers import utils

logger = logging.getLogger(__name__)

class CreatedLoanHandler(EventHandler):
    signature = 'CreatedLoan(uint256,address,address)'
    signature_hash = web3.Web3.sha3(text=signature)

    def _parse(self):
        data = self._event.get('data')[2:]
        splited_args = utils.split_every(64, data)
        self._index = utils.to_int(splited_args[0])
        self._borrower = utils.to_address(splited_args[1])
        self._creator = utils.to_address(splited_args[2])
        self._block_number = self._event.get('blockNumber')
        self._transaction = self._event.get('transactionHash').hex()

    def do(self):
        # TODO: Fix requests.exceptions.ChunkedEncodingError: ('Connection broken: IncompleteRead(0 bytes read)', IncompleteRead(0 bytes read))
        self._logger.info("Calling Loan public functions for loan {}".format(self._index))
        incomplete_loan = True
        while incomplete_loan:
            d_init = dt.now()
            try:
                d = async_fill_loan(self._contract, self._w3, self._index, self._block_number)
            except Exception as e:
                self._logger.error(e.message, exc_info=True)
            finally:
                incomplete_loan = False if len(d) == 12 else True
                if incomplete_loan:
                    self._logger.info("Retry fill loan")

        d_fin = dt.now()

        self._logger.info("elapsed: {}".format(d_fin - d_init))


        # some rule
        # if len(d.get("expiration_requests")) > 30:
        #     return []
        # else:
        #     commit = Commit()
        #     commit.opcode = "loan_request"
        #     commit.timestamp = int(d['created'])
        #     commit.proof = self._transaction
        #     assert len(d) == 12, "Loan data not fully loaded"
        #
        #     commit.data = dict(d)
        #     return [commit]
        commit = Commit()
        commit.opcode = "loan_request"
        commit.timestamp = int(d['created'])
        commit.proof = self._transaction
        assert len(d) == 12, "Loan data not fully loaded"

        commit.data = dict(d)
        return [commit]


def fill_index(index, d):
    try:
        d['index'] = index
    except Exception as e:
        logger.debug("EXCEPTION: {}".format(e))
def fill_created(w3, block_number, d):
    try:
        d['created'] = str(w3.eth.getBlock(block_number).timestamp)
    except Exception as e:
        logger.debug("EXCEPTION: {}".format(e))
def fill_status(contract, index, d):
    try:
        d['status'] = contract.functions.getStatus(index).call()
    except Exception as e:
        logger.debug("EXCEPTION: {}".format(e))
def fill_oracle(contract, index, d):
    try:
        d['oracle'] = str(contract.functions.getOracle(index).call())
    except Exception as e:
        logger.debug("EXCEPTION: {}".format(e))
def fill_borrower(contract, index, d):
    try:
        d['borrower'] = str(contract.functions.getBorrower(index).call())
    except Exception as e:
        logger.debug("EXCEPTION: {}".format(e))
def fill_lender(contract, index, d):
    try:
        d['lender'] = str(contract.functions.ownerOf(index).call())
    except Exception as e:
        logger.debug("EXCEPTION: {}".format(e))
def fill_creator(contract, index, d):
    try:
        d['creator'] = str(contract.functions.getCreator(index).call())
    except Exception as e:
        logger.debug("EXCEPTION: {}".format(e))
def fill_cosigner(contract, index, d):
    try:
        d['cosigner'] = contract.functions.getCosigner(index).call().hex()
    except Exception as e:
        logger.debug("EXCEPTION: {}".format(e))
def fill_amount(contract, index, d):
    try:
        d['amount'] = str(contract.functions.getAmount(index).call())
    except Exception as e:
        logger.debug("EXCEPTION: {}".format(e))
def fill_interest(contract, index, d):
    try:
        d['interest'] = str(contract.functions.getInterest(index).call())
    except Exception as e:
        logger.debug("EXCEPTION: {}".format(e))
def fill_punitory_interest(contract, index, d):
    try:
        d['punitory_interest'] = str(contract.functions.getPunitoryInterest(index).call())
    except Exception as e:
        logger.debug("EXCEPTION: {}".format(e))
def fill_interest_timestamp(contract, index, d):
    try:
        d['interest_timestamp'] = str(contract.functions.getInterestTimestamp(index).call())
    except Exception as e:
        logger.debug("EXCEPTION: {}".format(e))
def fill_paid(contract, index, d):
    try:
        d['paid'] = str(contract.functions.getPaid(index).call())
    except Exception as e:
        logger.debug("EXCEPTION: {}".format(e))
def fill_interest_rate(contract, index, d):
    try:
        d['interest_rate'] = str(contract.functions.getInterestRate(index).call())
    except Exception as e:
        logger.debug("EXCEPTION: {}".format(e))
def fill_interest_rate_punitory(contract, index, d):
    try:
        d['interest_rate_punitory'] = str(contract.functions.getInterestRatePunitory(index).call())
    except Exception as e:
        logger.debug("EXCEPTION: {}".format(e))
def fill_due_time(contract, index, d):
    try:
        d['due_time'] = str(dt.utcfromtimestamp(contract.functions.getDueTime(index).call()))
    except Exception as e:
        logger.debug("EXCEPTION: {}".format(e))
def fill_dues_in(contract, index, d):
    try:
        d['dues_in'] = str(contract.functions.getDuesIn(index).call())
    except Exception as e:
        logger.debug("EXCEPTION: {}".format(e))
def fill_currency(contract, index, d):
    try:
        d['currency'] = contract.web3.toHex(contract.functions.getCurrency(index).call())
    except Exception as e:
        logger.debug("EXCEPTION: {}".format(e))
def fill_cancelable_at(contract, index, d):
    try:
        d['cancelable_at'] = str(contract.functions.getCancelableAt(index).call())
    except Exception as e:
        logger.debug("EXCEPTION: {}".format(e))
def fill_lender_balance(contract, index, d):
    try:
        d['lender_balance'] = str(contract.functions.getLenderBalance(index).call())
    except Exception as e:
        logger.debug("EXCEPTION: {}".format(e))
def fill_expiration_requests(contract, index, d):
    try:
        d['expiration_requests'] = str(contract.functions.getExpirationRequest(index).call())
    except Exception as e:
        logger.debug("EXCEPTION: {}".format(e))
def fill_approved_transfer(contract, index, d):
    try:
        d['approved_transfer'] = contract.functions.getApproved(index).call().hex()
    except Exception as e:
        logger.debug("EXCEPTION: {}".format(e))


def async_fill_loan(contract, w3, index, block_number):
    manager = Manager()
    loan = manager.dict()

    process = []
    process.append(Process(target=fill_index, args=(index, loan)))
    process.append(Process(target=fill_created, args=(w3, block_number, loan)))
    process.append(Process(target=fill_oracle, args=(contract, index, loan)))
    process.append(Process(target=fill_borrower, args=(contract, index, loan)))
    process.append(Process(target=fill_creator, args=(contract, index, loan)))
    process.append(Process(target=fill_amount, args=(contract, index, loan)))
    process.append(Process(target=fill_interest_rate, args=(contract, index, loan)))
    process.append(Process(target=fill_interest_rate_punitory, args=(contract, index, loan)))
    process.append(Process(target=fill_dues_in, args=(contract, index, loan)))
    process.append(Process(target=fill_currency, args=(contract, index, loan)))
    process.append(Process(target=fill_cancelable_at, args=(contract, index, loan)))
    process.append(Process(target=fill_expiration_requests, args=(contract, index, loan)))

    try:
        for proc in process:
            proc.start()

        for proc in process:
            proc.join()
    except ProcessError as e:
        raise Exception(e.message)
    except Exception as e:
        raise Exception(e.message)
    return loan