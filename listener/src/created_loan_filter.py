import random
import json
import web3
from web3 import Web3
from web3.utils.events import get_event_data
import functools


class CreatedLoanFilter(object):
    @staticmethod
    def instantiate(config_path):
        config = json.load(open(config_path, 'r'))
        url_node = config['URL_NODE']
        contract_address = config['CONTRACT_ADDRESS']
        abi = config['ABI']

        node_provider = web3.HTTPProvider(url_node)
        w3 = Web3(node_provider)
        contract = w3.eth.contract(
            address=w3.toChecksumAddress(contract_address),
            abi=abi
        )

        log_filter = w3.eth.filter(filter_id=config['FILTER_ID'])
        log_data_extract_fn = functools.partial(get_event_data, contract.events.CreatedLoan().abi)
        log_filter.log_entry_formatter = log_data_extract_fn

        return log_filter

    @staticmethod
    def create(config_path):
        config = json.load(open(config_path, 'r'))
        url_node = config['URL_NODE']
        contract_address = config['CONTRACT_ADDRESS']
        abi = config['ABI']

        node_provider = web3.HTTPProvider(url_node)
        w3 = Web3(node_provider)
        contract = w3.eth.contract(
            address=w3.toChecksumAddress(contract_address),
            abi=abi
        )

        log_filter = contract.events.CreatedLoan.createFilter(fromBlock=0)

        config['FILTER_ID'] = log_filter.filter_id
        json.dump(config, open(config_path, 'w'), indent=4, sort_keys=True)

        return log_filter

    @staticmethod
    def remove(config_path):
        config = json.load(open(config_path, 'r'))
        url_node = config['URL_NODE']
        contract_address = config['CONTRACT_ADDRESS']
        abi = config['ABI']
        filter_id = config['FILTER_ID']

        node_provider = web3.HTTPProvider(url_node)
        w3 = Web3(node_provider)
        contract = w3.eth.contract(
            address=w3.toChecksumAddress(contract_address),
            abi=abi
        )

        uninstalled = w3.eth.uninstallFilter(filter_id)

        if uninstalled:
            config['FILTER_ID'] = None

            json.dump(config, open(config_path, 'w'), indent=4, sort_keys=True)

        return uninstalled



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
            '_index' : str(self.__get_new_index()),
            '_borrower': '0x00bd67f06685ad070579b95c2e19ec0022fc916e',
            '_creator': '0x00bd67f06685ad070579b95c2e19ec0022fc916e'
        }

        entry["args"] = args

        return entry