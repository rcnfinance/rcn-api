import web3

from datetime import datetime as dt
from multiprocessing import Manager
from multiprocessing import Process
from .event_handler import EventHandler
from models import Commit
from handlers import utils


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
        self._transaction = str(self._event.get('transactionHash'))

    def do(self):
        self._logger.info("Calling Loan public functions for loan {}".format(self._index))
        d_init = dt.now()
        d = async_fill_loan(self._contract, self._w3, self._index, self._block_number)
        d_fin = dt.now()
        self._logger.info("elapsed: {}".format(d_fin - d_init))

        commit = Commit()
        commit.opcode = "loan_request"
        commit.timestamp = int(d['created'])
        commit.order = Commit.objects.count()
        commit.proof = self._transaction
        assert len(d) == 12, "Loan data not fully loaded"

        commit.data = dict(d)
        commit.save()

def fill_index(index, d):
    d['index'] = index
def fill_created(w3, block_number, d):
    d['created'] = str(w3.eth.getBlock(block_number).timestamp)
def fill_status(contract, index, d):
    d['status'] = contract.functions.getStatus(index).call()
def fill_oracle(contract, index, d):
    d['oracle'] = str(contract.functions.getOracle(index).call())
def fill_borrower(contract, index, d):
    d['borrower'] = str(contract.functions.getBorrower(index).call())
def fill_lender(contract, index, d):
    d['lender'] = str(contract.functions.ownerOf(index).call())
def fill_creator(contract, index, d):
    d['creator'] = str(contract.functions.getCreator(index).call())
def fill_cosigner(contract, index, d):
    d['cosigner'] = str(contract.functions.getCosigner(index).call())
def fill_amount(contract, index, d):
    d['amount'] = str(contract.functions.getAmount(index).call())
def fill_interest(contract, index, d):
    d['interest'] = str(contract.functions.getInterest(index).call())
def fill_punitory_interest(contract, index, d):
    d['punitory_interest'] = str(contract.functions.getPunitoryInterest(index).call())
def fill_interest_timestamp(contract, index, d):
    d['interest_timestamp'] = str(contract.functions.getInterestTimestamp(index).call())
def fill_paid(contract, index, d):
    d['paid'] = str(contract.functions.getPaid(index).call())
def fill_interest_rate(contract, index, d):
    d['interest_rate'] = str(contract.functions.getInterestRate(index).call())
def fill_interest_rate_punitory(contract, index, d):
    d['interest_rate_punitory'] = str(contract.functions.getInterestRatePunitory(index).call())
def fill_due_time(contract, index, d):
    d['due_time'] = str(dt.utcfromtimestamp(contract.functions.getDueTime(index).call()))
def fill_dues_in(contract, index, d):
    d['dues_in'] = str(contract.functions.getDuesIn(index).call())
def fill_currency(contract, index, d):
    d['currency'] = str(contract.functions.getCurrency(index).call())
def fill_cancelable_at(contract, index, d):
    d['cancelable_at'] = str(contract.functions.getCancelableAt(index).call())
def fill_lender_balance(contract, index, d):
    d['lender_balance'] = str(contract.functions.getLenderBalance(index).call())
def fill_expiration_requests(contract, index, d):
    d['expiration_requests'] = str(contract.functions.getExpirationRequest(index).call())
def fill_approved_transfer(contract, index, d):
    d['approved_transfer'] = str(contract.functions.getApproved(index).call())

def async_fill_loan(contract, w3, index, block_number):
    manager = Manager()
    loan = manager.dict()

    process = []
    process.append(Process(target=fill_index, args=(index, loan)))
    process.append(Process(target=fill_created, args=(w3, block_number, loan)))
    # process.append(Process(target=fill_status, args=(contract, index, loan)))  # default 0
    process.append(Process(target=fill_oracle, args=(contract, index, loan)))
    process.append(Process(target=fill_borrower, args=(contract, index, loan)))
    # process.append(Process(target=fill_lender, args=(contract, index, loan)))  # default 0x0
    process.append(Process(target=fill_creator, args=(contract, index, loan)))
    # process.append(Process(target=fill_cosigner, args=(contract, index, loan)))  # default 0x0
    process.append(Process(target=fill_amount, args=(contract, index, loan)))
    # process.append(Process(target=fill_interest, args=(contract, index, loan)))  # default 0
    # process.append(Process(target=fill_punitory_interest, args=(contract, index, loan)))  # default 0
    # process.append(Process(target=fill_interest_timestamp, args=(contract, index, loan)))  # default 0
    # process.append(Process(target=fill_paid, args=(contract, index, loan)))  # default 0
    process.append(Process(target=fill_interest_rate, args=(contract, index, loan)))
    process.append(Process(target=fill_interest_rate_punitory, args=(contract, index, loan)))
    # process.append(Process(target=fill_due_time, args=(contract, index, loan)))  # default 0
    process.append(Process(target=fill_dues_in, args=(contract, index, loan)))
    process.append(Process(target=fill_currency, args=(contract, index, loan)))
    process.append(Process(target=fill_cancelable_at, args=(contract, index, loan)))
    # process.append(Process(target=fill_lender_balance, args=(contract, index, loan)))  # default 0
    process.append(Process(target=fill_expiration_requests, args=(contract, index, loan)))
    # process.append(Process(target=fill_approved_transfer, args=(contract, index, loan)))  # default 0x0

    for proc in process:
        proc.start()

    for proc in process:
        proc.join()

    return loan