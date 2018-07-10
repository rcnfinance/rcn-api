from datetime import datetime as dt
from multiprocessing import Manager
from multiprocessing import Process
import web3
from .event_handler import EventHandler
from models import Loan
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

    def do(self):
        self._logger.info("Calling Loan public functions for loan {}".format(self._index))
        d_init = dt.now()
        d = async_fill_loan(self._contract, self._w3, self._index, self._block_number)
        d_fin = dt.now()
        self._logger.info("elapsed: {}".format(d_fin - d_init))
        loan = Loan(**d)
        # loan = Loan()
        # loan.index = str(self._index)
        # loan.created = str(dt.utcfromtimestamp(w3.eth.getBlock(self._block_number).timestamp))
        # loan.status = str(contract.functions.getStatus(self._index).call())
        # loan.oracle = str(contract.functions.getOracle(self._index).call())
        # loan.borrower = str(contract.functions.getBorrower(self._index).call())
        # loan.lender = str(contract.functions.ownerOf(self._index).call())
        # loan.creator = str(contract.functions.getCreator(self._index).call())
        # loan.cosigner = str(contract.functions.getCosigner(self._index).call())
        # loan.amount = str(contract.functions.getAmount(self._index).call())
        # loan.interest = str(contract.functions.getInterest(self._index).call())
        # loan.punitory_interest = str(contract.functions.getPunitoryInterest(self._index).call())
        # loan.interest_timestamp = str(contract.functions.getInterestTimestamp(self._index).call())
        # loan.paid = str(contract.functions.getPaid(self._index).call())
        # loan.interest_rate = str(contract.functions.getInterestRate(self._index).call())
        # loan.interest_rate_punitory = str(contract.functions.getInterestRatePunitory(self._index).call())
        # loan.due_time = str(dt.utcfromtimestamp(contract.functions.getDueTime(self._index).call()))
        # loan.dues_in = str(contract.functions.getDuesIn(self._index).call())
        # loan.currency = str(contract.functions.getCurrency(self._index).call())
        # loan.cancelable_at = str(contract.functions.getCancelableAt(self._index).call())
        # loan.lender_balance = str(contract.functions.getLenderBalance(self._index).call())
        # loan.expiration_requests = str(contract.functions.getExpirationRequest(self._index).call())

        loan.save()


def fill_index(index, d):
    d['index'] = str(index)
def fill_created(w3, block_number, d):
    d['created'] = str(dt.utcfromtimestamp(w3.eth.getBlock(block_number).timestamp))
def fill_status(contract, index, d):
    d['status'] = str(contract.functions.getStatus(index).call())
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

def async_fill_loan(contract, w3, index, block_number):
    manager = Manager()
    loan = manager.dict()

    process = []
    p1 = Process(target=fill_index, args=(index, loan))
    process.append(p1)
    p2 = Process(target=fill_created, args=(w3, block_number, loan))
    process.append(p2)
    p3 = Process(target=fill_status, args=(contract, index, loan))
    process.append(p3)
    p4 = Process(target=fill_oracle, args=(contract, index, loan))
    process.append(p4)
    p5 = Process(target=fill_borrower, args=(contract, index, loan))
    process.append(p5)
    p6 = Process(target=fill_lender, args=(contract, index, loan))
    process.append(p6)
    p7 = Process(target=fill_creator, args=(contract, index, loan))
    process.append(p7)
    p8 = Process(target=fill_cosigner, args=(contract, index, loan))
    process.append(p8)
    p9 = Process(target=fill_amount, args=(contract, index, loan))
    process.append(p9)
    p10 = Process(target=fill_interest, args=(contract, index, loan))
    process.append(p10)
    p11 = Process(target=fill_punitory_interest, args=(contract, index, loan))
    process.append(p11)
    p12 = Process(target=fill_interest_timestamp, args=(contract, index, loan))
    process.append(p12)
    p13 = Process(target=fill_paid, args=(contract, index, loan))
    process.append(p13)
    p14 = Process(target=fill_interest_rate, args=(contract, index, loan))
    process.append(p14)
    p15 = Process(target=fill_interest_rate_punitory, args=(contract, index, loan))
    process.append(p15)
    p16 = Process(target=fill_due_time, args=(contract, index, loan))
    process.append(p16)
    p17 = Process(target=fill_dues_in, args=(contract, index, loan))
    process.append(p17)
    p18 = Process(target=fill_currency, args=(contract, index, loan))
    process.append(p18)
    p19 = Process(target=fill_cancelable_at, args=(contract, index, loan))
    process.append(p19)
    p20 = Process(target=fill_lender_balance, args=(contract, index, loan))
    process.append(p20)
    p21 = Process(target=fill_expiration_requests, args=(contract, index, loan))
    process.append(p21)

    for proc in process:
        proc.start()

    for proc in process:
        proc.join()

    return loan