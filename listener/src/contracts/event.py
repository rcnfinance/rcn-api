import logging
import web3


class EventHandler():
    def __init__(self, contract_conn, event):
        self._event = event
        self._event_name = self.signature.split("(")[0]
        self._contract_conn = contract_conn
        self._logger = logging.getLogger(self.__class__.__name__)
        self._contract_abi = self._contract_conn.abi
        self._parse()
        self._normalize()

    def _parse(self):
        self._logger.info("event: {}".format(self._event))

        self._event_abi = web3.utils.abi.filter_by_name(self._event_name, self._contract_abi)[0]
        self._args = dict(web3.utils.events.get_event_data(self._event_abi, self._event).args)
        self._block_number = self._event.get('blockNumber')
        self._transaction = self._event.get('transactionHash').hex()

    def _parse(self):
        ropsten_abi = [
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "name": "_from",
                        "type": "address"
                    },
                    {
                        "indexed": True,
                        "name": "_to",
                        "type": "address"
                    },
                    {
                        "indexed": False,
                        "name": "_tokenId",
                        "type": "uint256"
                    }
                ],
                "name": "Transfer",
                "type": "event"
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "name": "_owner",
                        "type": "address"
                    },
                    {
                        "indexed": True,
                        "name": "_approved",
                        "type": "address"
                    },
                    {
                        "indexed": False,
                        "name": "_tokenId",
                        "type": "uint256"
                    }
                ],
                "name": "Approval",
                "type": "event"
            },
        ]

        if self._contract_conn.address == "0xe4BfBBB04844cdEbd6b7814183f92E0703257d48" and self._event_name in ["Transfer", "A"]:  ## ropsten address
            self._logger.warning("DEBT ENGINE FROM ROPSTEN PARCHE!!!!")
            self._event_abi = web3.utils.abi.filter_by_name(self._event_name, ropsten_abi)[0]
        else:
            self._event_abi = web3.utils.abi.filter_by_name(self._event_name, self._contract_abi)[0]

        self._args = dict(web3.utils.events.get_event_data(self._event_abi, self._event).args)
        self._block_number = self._event.get('blockNumber')
        self._transaction = self._event.get('transactionHash').hex()

    def _normalize(self):
        pass

    def handle(self):
        raise NotImplementedError()

    def _block_timestamp(self):
        return self._contract_conn.w3.eth.getBlock(self._block_number).timestamp
