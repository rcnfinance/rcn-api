import os
import json
from datetime import datetime as dt
import time
from multiprocessing import Process, Manager
import web3
from web3 import Web3

CONFIG_FILENAME = 'config_created_loan.json'


def open_config(config_filename):
    return json.load(open(config_filename, 'r'))

def actualize_config(config, config_filename):
    json.dump(config, open(config_filename, 'w'), indent=4, sort_keys=True)

def handle_event(event):
    # event CreatedLoan(uint _index, address _borrower, address _creator);
    print(event)
    # loan = async_fill_loan(event)
    loan = fill_loan(event)
    print(loan)
    assert len(loan.keys()) == 21

def main_loop(event_filter, interval_sleep):
    while True:
        new_entries = event_filter.get_new_entries()
        print('There are {} new new_entries'.format(len(new_entries)))
        for event in new_entries:
            handle_event(event)
        time.sleep(interval_sleep)

def main(config_filename):
    config_listener = open_config(config_filename)
    URL_NODE = config_listener['URL_NODE']
    CONTRACT_ADDRESS = config_listener['CONTRACT_ADDRESS']
    ABI = config_listener['ABI']
    
    node_provider = web3.HTTPProvider(URL_NODE)
    w3 = Web3(node_provider)
    contract = w3.eth.contract(
        address=w3.toChecksumAddress(CONTRACT_ADDRESS),
        abi=ABI
    )

    if config_listener['FILTER_ID']:
        FILTER_ID = config_listener['FILTER_ID']
    else:
        config_listener['FILTER_ID'] = create_filter(contract.events.CreatedLoan)
        FILTER_ID = config_listener['FILTER_ID']
        actualize_config(config_listener, config_filename)


    event_filter = w3.eth.filter(filter_id=FILTER_ID)

    main_loop(event_filter, 10)

# Custom function event created_loan
def fill_index(index, d):
    d['index'] = index
def fill_created(block_number, d):
    d['created'] = dt.utcfromtimestamp(w3.eth.getBlock(block_number).timestamp)
def fill_status(index, d):
    d['status'] = str(contract.functions.getStatus(index).call())
def fill_oracle(index, d):
    d['oracle'] = contract.functions.getOracle(index).call()
def fill_borrower(index, d):
    d['borrower'] = contract.functions.getBorrower(index).call()
def fill_lender(index, d):
    d['lender'] = contract.functions.ownerOf(index).call()
def fill_creator(index, d):
    d['creator'] = contract.functions.getCreator(index).call()
def fill_cosigner(index, d):
    d['cosigner'] = contract.functions.getCosigner(index).call()
def fill_amount(index, d):
    d['amount'] = contract.functions.getAmount(index).call()
def fill_interest(index, d):
    d['interest'] = contract.functions.getInterest(index).call()
def fill_punitory_interest(index, d):
    d['punitory_interest'] = contract.functions.getPunitoryInterest(index).call()
def fill_interest_timestamp(index, d):
    d['interest_timestamp'] = contract.functions.getInterestTimestamp(index).call()
def fill_paid(index, d):
    d['paid'] = contract.functions.getPaid(index).call()
def fill_interest_rate(index, d):
    d['interest_rate'] = contract.functions.getInterestRate(index).call()
def fill_interest_rate_punitory(index, d):
    d['interest_rate_punitory'] = contract.functions.getInterestRatePunitory(index).call()
def fill_due_time(index, d):
    d['due_time'] = dt.utcfromtimestamp(contract.functions.getDueTime(index).call())
def fill_dues_in(index, d):
    d['dues_in'] = contract.functions.getDuesIn(index).call()
def fill_currency(index, d):
    d['currency'] = contract.functions.getCurrency(index).call()
def fill_cancelable_at(index, d):
    d['cancelable_at'] = contract.functions.getCancelableAt(index).call()
def fill_lender_balance(index, d):
    d['lender_balance'] = contract.functions.getLenderBalance(index).call()
def fill_expiration_requests(index, d):
    d['expiration_requests'] = contract.functions.getExpirationRequest(index).call()

def fill_loan(event):
    loan = dict()
    index = event.args._index
    block_number = event.blockNumber
    loan['index'] = index
    loan['created'] = dt.utcfromtimestamp(w3.eth.getBlock(block_number).timestamp)
    loan['status'] = str(contract.functions.getStatus(index).call())
    loan['oracle'] = contract.functions.getOracle(index).call()
    loan['borrower'] = contract.functions.getBorrower(index).call()
    loan['lender'] = contract.functions.ownerOf(index).call()
    loan['creator'] = contract.functions.getCreator(index).call()
    loan['cosigner'] = contract.functions.getCosigner(index).call()
    loan['amount'] = contract.functions.getAmount(index).call()
    loan['interest'] = contract.functions.getInterest(index).call()
    loan['punitory_interest'] = contract.functions.getPunitoryInterest(index).call()
    loan['interest_timestamp'] = contract.functions.getInterestTimestamp(index).call()
    loan['paid'] = contract.functions.getPaid(index).call()
    loan['interest_rate'] = contract.functions.getInterestRate(index).call()
    loan['interest_rate_punitory'] = contract.functions.getInterestRatePunitory(index).call()
    loan['due_time'] = dt.utcfromtimestamp(contract.functions.getDueTime(index).call())
    loan['dues_in'] = contract.functions.getDuesIn(index).call()
    loan['currency'] = contract.functions.getCurrency(index).call()
    loan['cancelable_at'] = contract.functions.getCancelableAt(index).call()
    loan['lender_balance'] = contract.functions.getLenderBalance(index).call()
    loan['expiration_requests'] = contract.functions.getExpirationRequest(index).call()

    for key, value in loan.items():
        loan[key] = str(value)

    return loan


def async_fill_loan(event):
    manager = Manager()
    loan = manager.dict()

    process = []
    p1 = Process(target=fill_index, args=(event.args._index, loan))
    process.append(p1)
    p2 = Process(target=fill_created, args=(event.blockNumber, loan))
    process.append(p2)
    p3 = Process(target=fill_status, args=(event.args._index, loan))
    process.append(p3)
    p4 = Process(target=fill_oracle, args=(event.args._index, loan))
    process.append(p4)
    p5 = Process(target=fill_borrower, args=(event.args._index, loan))
    process.append(p5)
    p6 = Process(target=fill_lender, args=(event.args._index, loan))
    process.append(p6)
    p7 = Process(target=fill_creator, args=(event.args._index, loan))
    process.append(p7)
    p8 = Process(target=fill_cosigner, args=(event.args._index, loan))
    process.append(p8)
    p9 = Process(target=fill_amount, args=(event.args._index, loan))
    process.append(p9)
    p10 = Process(target=fill_interest, args=(event.args._index, loan))
    process.append(p10)
    p11 = Process(target=fill_punitory_interest, args=(event.args._index, loan))
    process.append(p11)
    p12 = Process(target=fill_interest_timestamp, args=(event.args._index, loan))
    process.append(p12)
    p13 = Process(target=fill_paid, args=(event.args._index, loan))
    process.append(p13)
    p14 = Process(target=fill_interest_rate, args=(event.args._index, loan))
    process.append(p14)
    p15 = Process(target=fill_interest_rate_punitory, args=(event.args._index, loan))
    process.append(p15)
    p16 = Process(target=fill_due_time, args=(event.args._index, loan))
    process.append(p16)
    p17 = Process(target=fill_dues_in, args=(event.args._index, loan))
    process.append(p17)
    p18 = Process(target=fill_currency, args=(event.args._index, loan))
    process.append(p18)
    p19 = Process(target=fill_cancelable_at, args=(event.args._index, loan))
    process.append(p19)
    p20 = Process(target=fill_lender_balance, args=(event.args._index, loan))
    process.append(p20)
    p21 = Process(target=fill_expiration_requests, args=(event.args._index, loan))
    process.append(p21)

    for proc in process:
        proc.start()

    for proc in process:
        proc.join()

    return loan

def create_filter(contract_event, argument_filters=None, fromBlock=0, toBlock='latest'):
    event = contract_event.createFilter(argument_filters=argument_filters, fromBlock=fromBlock, toBlock=toBlock)
    return event.filter_id


if __name__ == '__main__':
    main(CONFIG_FILENAME)
