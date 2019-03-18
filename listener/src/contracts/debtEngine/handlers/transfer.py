import web3
from contracts.event import EventHandler
from models import Commit


class Transfer(EventHandler):
    signature = "Transfer(address,address,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()


    # def _parse(self):
    #     data = self._event.get("data")[2:]
    #     self._from = utils.to_address(web3.Web3.toHex(self._event.get("topics")[1]))
    #     self._to = utils.to_address(web3.Web3.toHex(self._event.get("topics")[2]))
    #     self._token_id = "0x" + data
    #     self._block_number = self._event.get('blockNumber')
    #     self._transaction = self._event.get('transactionHash').hex()


    def handle(self):
        print(self._args)
        print(self._event)
        if self._args.get("_from") != "0x0000000000000000000000000000000000000000":

            commit = Commit()

            commit.opcode = "transfer_debt_engine"
            commit.timestamp = self._block_timestamp()
            commit.proof = self._transaction

            data = {
                "id": self._event.get("data"),
                "from": self._args.get("_from"),
                "to": self._args.get("_to")
            }

            commit.data = data

            return [commit]
        else:
            return []
