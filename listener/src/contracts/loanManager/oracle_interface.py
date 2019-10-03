import os
import web3


class OracleInterface():
    ABI = [{'constant': True,
            'inputs': [],
            'name': 'currency',
            'outputs': [{'internalType': 'bytes32', 'name': '', 'type': 'bytes32'}],
            'payable': False,
            'stateMutability': 'view',
            'type': 'function'}]

    def __init__(self, contract_address):
        self._provider = web3.HTTPProvider(os.environ.get("URL_NODE"))
        self._w3 = web3.Web3(self._provider)
        self._contract = self._w3.eth.contract(
            address=contract_address,
            abi=self.ABI
        )

    def currency(self):
        currency = self._contract.functions.currency().call()
        hex_currency = web3.utils.contracts.encode_hex(currency)
        return hex_currency
