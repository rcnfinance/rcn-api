import json
import web3


class EthereumConnection():
    def __init__(self, url_node):
        self._url_node = url_node
        self._node_provider = web3.HTTPProvider(self._url_node)
        self._w3 = web3.Web3(self._node_provider)

    @property
    def w3(self):
        return self._w3

    @property
    def url_node(self):
        return self._url_node


class ContractConnection():
    def __init__(self, eth_conn, contract_address, abi_path):
        self._eth_conn = eth_conn
        self._contract_address = self._eth_conn.w3.toChecksumAddress(contract_address)
        self._abi_path = abi_path

        self.__json_abi = self.__open_abi()
        self._contract = self._eth_conn.w3.eth.contract(
            address=self._contract_address,
            abi=self.__json_abi
        )

    def __open_abi(self):
        return json.load(open(self._abi_path, "r"))

    @property
    def abi(self):
        return self.__json_abi

    @property
    def contract(self):
        return self._contract

    @property
    def address(self):
        return self._contract_address

    @property
    def eth(self):
        return self._contract.web3.eth

    @property
    def w3(self):
        return self._eth_conn.w3
