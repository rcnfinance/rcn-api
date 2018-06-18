import json
import random
from datetime import datetime as dt
import time
import requests
import web3
from web3 import Web3
from web3.utils.events import get_event_data
import functools



CONFIG_PATH = 'config_created_loan.json'
DEV_NODE_ROPSTEN = "https://ropsten.node.rcn.loans:8545/"
CONTRACT_ADDRESS = '0xbee217bfe06c6faaa2d5f2e06ebb84c5fb70d9bf'

config = json.load(open(CONFIG_PATH))
ropsten_provider = web3.HTTPProvider(DEV_NODE_ROPSTEN)
w3 = Web3(ropsten_provider)
contract = w3.eth.contract(
    address=w3.toChecksumAddress(CONTRACT_ADDRESS),
    abi=config.get('ABI')
)

print(contract.functions.getTotalLoans().call())
# f = contract.events.CreatedLoan.createFilter(fromBlock=0)
# print(f.filter_id)
#
# g = w3.eth.filter(filter_id=f.filter_id)
# print(g.filter_id)
# log_data_extract_fn = functools.partial(get_event_data, contract.events.CreatedLoan().abi)
# g.log_entry_formatter = log_data_extract_fn


# w3.eth.uninstallFilter(f.filter_id)
# w3.eth.uninstallFilter(g.filter_id)


def fill_loan(self, event):
    loan = dict()
    index = event.get('args').get('_index')
    block_number = event.get('blockNumber')
    loan['index'] = index
    loan['created'] = dt.utcfromtimestamp(self._w3.eth.getBlock(block_number).timestamp)
    loan['status'] = str(self._contract.functions.getStatus(index).call())
    loan['oracle'] = self._contract.functions.getOracle(index).call()
    loan['borrower'] = self._contract.functions.getBorrower(index).call()
    loan['lender'] = self._contract.functions.ownerOf(index).call()
    loan['creator'] = self._contract.functions.getCreator(index).call()
    loan['cosigner'] = self._contract.functions.getCosigner(index).call()
    loan['amount'] = self._contract.functions.getAmount(index).call()
    loan['interest'] = self._contract.functions.getInterest(index).call()
    loan['punitory_interest'] = self._contract.functions.getPunitoryInterest(index).call()
    loan['interest_timestamp'] = self._contract.functions.getInterestTimestamp(index).call()
    loan['paid'] = self._contract.functions.getPaid(index).call()
    loan['interest_rate'] = self._contract.functions.getInterestRate(index).call()
    loan['interest_rate_punitory'] = self._contract.functions.getInterestRatePunitory(index).call()
    loan['due_time'] = dt.utcfromtimestamp(self._contract.functions.getDueTime(index).call())
    loan['dues_in'] = self._contract.functions.getDuesIn(index).call()
    loan['currency'] = self._contract.functions.getCurrency(index).call()
    loan['cancelable_at'] = self._contract.functions.getCancelableAt(index).call()
    loan['lender_balance'] = self._contract.functions.getLenderBalance(index).call()
    loan['expiration_requests'] = self._contract.functions.getExpirationRequest(index).call()

    for key, value in loan.items():
        loan[key] = str(value)

    return loan

class APIPreserver(object):
    def __init__(self):
        self._url = "http://10.0.4.120:8000/v1/loan/"
        self._headers = {
            'Content-Type': "application/json"
        }

    def preserve(self, data):
        response = requests.post(self._url, json=data, headers=self._headers)
        return response.status_code, response.text


class Handler(object):
    def __init__(self, config_filename, preservers):
        self.__init_environment(config_filename)
        self._preservers = preservers

    def __init_environment(self, config_filename):
        self._config = self._open_config(config_filename)

        self._url_node = self._config['URL_NODE']
        self._contract_address = self._config['CONTRACT_ADDRESS']
        self._abi = self._config['ABI']

        self._node_provider = web3.HTTPProvider(self._url_node)
        self._w3 = Web3(self._node_provider)
        self._contract = self._w3.eth.contract(
            address=self._w3.toChecksumAddress(self._contract_address),
            abi=self._abi
        )

        def _open_config(self, config_filepath):
            return json.load(open(config_filepath, 'r'))

        def handle(self, event):
            parsed_loan = self._parse_event(event)
            self._save(parsed_loan)

        def _parse_event(event):
            raise NotImplementedError()

        def _save(self, parsed_loan):
            for preserver in self._preservers:
                preserver.preserve(parsed_loan)


class HandlerCreateLoan(Handler):
    def _parse_event(self, event):
        # loan = dict()
        # index = event.get('args').get('_index')
        # block_number = event.get('blockNumber')
        # loan['index'] = index
        # loan['created'] = dt.utcfromtimestamp(self._w3.eth.getBlock(block_number).timestamp)
        # loan['status'] = str(self._contract.functions.getStatus(index).call())
        # loan['oracle'] = self._contract.functions.getOracle(index).call()
        # loan['borrower'] = self._contract.functions.getBorrower(index).call()
        # loan['lender'] = self._contract.functions.ownerOf(index).call()
        # loan['creator'] = self._contract.functions.getCreator(index).call()
        # loan['cosigner'] = self._contract.functions.getCosigner(index).call()
        # loan['amount'] = self._contract.functions.getAmount(index).call()
        # loan['interest'] = self._contract.functions.getInterest(index).call()
        # loan['punitory_interest'] = self._contract.functions.getPunitoryInterest(index).call()
        # loan['interest_timestamp'] = self._contract.functions.getInterestTimestamp(index).call()
        # loan['paid'] = self._contract.functions.getPaid(index).call()
        # loan['interest_rate'] = self._contract.functions.getInterestRate(index).call()
        # loan['interest_rate_punitory'] = self._contract.functions.getInterestRatePunitory(index).call()
        # loan['due_time'] = dt.utcfromtimestamp(self._contract.functions.getDueTime(index).call())
        # loan['dues_in'] = self._contract.functions.getDuesIn(index).call()
        # loan['currency'] = self._contract.functions.getCurrency(index).call()
        # loan['cancelable_at'] = self._contract.functions.getCancelableAt(index).call()
        # loan['lender_balance'] = self._contract.functions.getLenderBalance(index).call()
        # loan['expiration_requests'] = self._contract.functions.getExpirationRequest(index).call()
        #
        # for key, value in loan.items():
        #     loan[key] = str(value)

        loan = {
            "amount": "200000000000000000000",
            "borrower": "0x35d803F11E900fb6300946b525f0d08D1Ffd4bed",
            "cancelable_at": "1970-01-03 00:00:00",
            "cosigner": "0x0000000000000000000000000000000000000000",
            "created": "2016-11-20 11:48:50",
            "creator": "0x35d803F11E900fb6300946b525f0d08D1Ffd4bed",
            "currency": "\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00",
            "due_time": "2018-05-21 20:42:59",
            "dues_in": "1970-01-13 00:00:00",
            "expiration_requests": "2018-06-05 19:40:58",
            "index": event.get('args').get('_index'),
            "interest": "1533334812242862439",
            "interest_rate": "13523478260869",
            "interest_rate_punitory": "12441600000000",
            "interest_timestamp": "2018-06-04 20:57:31",
            "lender": "0x35d803F11E900fb6300946b525f0d08D1Ffd4bed",
            "lender_balance": "0",
            "oracle": "0x0000000000000000000000000000000000000000",
            "paid": "122000000000000000000",
            "punitory_interest": "1423141359661568706",
            "status": "1"
        }

        return loan




class FakeCreatedLoanFilter(object):
    MIN_RANDOM_ENTRY = 0
    MAX_RANDOM_ENTRY = 3

    def __init__(self):
        self.__index = 0
        self.__entries = []

    def get_new_entries(self):
        random_cant_new_entries = random.randint(
            FakeCreatedLoanFilter.MIN_RANDOM_ENTRY,
            FakeCreatedLoanFilter.MAX_RANDOM_ENTRY
        )
        new_entries = []
        for i in range(random_cant_new_entries):
            random_entry = self.__generate_random_entry()
            new_entries.append(random_entry)
        self.__entries.extend(new_entries)
        return new_entries

    def get_all_entries(self):
        return self.__entries

    def __get_new_index(self):
        self.__index += 1
        return self.__index

    def __generate_random_entry(self):
        entry = {}
        entry["logIndex"] = "0"
        entry["transactionIndex"] = "0"
        entry["transactionHash"] = '0xe2e44b73d67147fb9988dce58d7616da759660a7fde99b3068c6b92fdb9ad8d3'
        entry["blockHash"] = '0x3a28c6909d44f380a2c64601ecbc3523551ed3840f3afd2549d72d0b710fbb2d'
        entry["blockNumber"] = "38"
        entry["address"] = '0x97c553ef6d28b88e19f47735c35369d71f891d76'
        entry["type"] = 'mined'
        entry["event"] = 'CreatedLoan'
        args = {
            '_index' : "self.__get_new_index()",
            '_borrower': '0x00bd67f06685ad070579b95c2e19ec0022fc916e',
            '_creator': '0x00bd67f06685ad070579b95c2e19ec0022fc916e'
        }

        entry["args"] = args

        return entry


class EventListener(object):
    """docstring for EventListener"""

    def __init__(self, config_filename, filter_log, handler):
        super(EventListener, self).__init__()
        self._filter = filter_log
        self._handler = handler
        self._config_filename = config_filename

        self._initialize()

    def _initialize(self):
        self._config = self._open_config()
        self._url_node = self._config['URL_NODE']
        self._contract_address = self._config['CONTRACT_ADDRESS']
        self._abi = self._config['ABI']

        self._node_provider = web3.HTTPProvider(self._url_node)
        self._w3 = Web3(self._node_provider)
        self._contract = self._w3.eth.contract(
            address=self._w3.toChecksumAddress(self._contract_address),
            abi=self._abi
        )

    def _open_config(self):
        return json.load(open(self._config_filename, 'r'))

    def _actualize_config(self):
        json.dump(self._config, open(self._config_filename, 'w'), indent=4, sort_keys=True)

    def main_loop(self, interval_sleep=10):
        while True:
            new_entries = self._filter.get_new_entries()
            print('There are {} new new_entries'.format(len(new_entries)))
            for event in new_entries:
                self._handler.handle(event)
            time.sleep(interval_sleep)

def main():
    CONFIG_PATH = "config_created_loan.json"
    created_loan_filter = FakeCreatedLoanFilter()
    api_preserver = APIPreserver()
    created_loan_handler = HandlerCreateLoan(CONFIG_PATH, [api_preserver])
    listener = EventListener(
        CONFIG_PATH,
        created_loan_filter,
        created_loan_handler
    )

    listener.main_loop(5)